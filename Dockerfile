FROM python:3.10

# Install system dependencies (optimized)
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    zlib1g-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    libffi-dev \
    curl

# Install nodejs and less manually (replaces node-less)
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g less less-plugin-clean-css

# Create odoo user
RUN useradd -m -d /opt/odoo -U -r -s /bin/bash odoo

WORKDIR /opt/odoo

# Install python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy addons
COPY official_addons /opt/odoo/official_addons
COPY custom /opt/odoo/custom

# Expose port
EXPOSE 8069

CMD ["python3", "odoo-bin", "-c", "odoo.conf"]
