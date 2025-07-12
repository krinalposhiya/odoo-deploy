/** @odoo-module */
import { registry } from '@web/core/registry';
const { Component, onWillStart, onMounted, useState, useRef } = owl
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";
import { loadJS } from "@web/core/assets";
import { _t } from "@web/core/l10n/translation";

export class product_gallary_dashboard extends Component {
  setup() {
    this.action = useService("action");
    this.orm = useService("orm");
    this.rpc = this.env.services.rpc
    this.state = useState({
      company_currency: 'USD',

    })
    onMounted(this.onMounted);
    onWillStart(this.onWillStart)

  }

  async onWillStart() {
    // await this.getInsuranceCardData()
    await this._loadProductDashboard()

    await this.getGreetings()
    await loadJS("https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js")
  }

  async getGreetings() {
    var self = this;
    const now = new Date();
    const hours = now.getHours();
    if (hours >= 5 && hours < 12) {
      self.greetings = "Good Morning";
    }
    else if (hours >= 12 && hours < 18) {
      self.greetings = "Good Afternoon";
    }
    else {
      self.greetings = "Good Evening";
    }
  }

  async onMounted() {
    this._loadProductDashboard();

  }


    async  _loadProductDashboard() {
    const categoryList = document.querySelector("#category-list");
    const productList = document.querySelector("#product-list");
    const searchInput = document.querySelector("#product-search");

    if (!categoryList || !productList) {
      console.warn("DOM elements not found.");
      return;
    }

    const categoryData = await rpc("/product/dashboard/data", {});
    const categories = categoryData.categories;

    categoryList.innerHTML = "";

    categories.forEach(cat => {
      const catDiv = document.createElement("div");
      catDiv.className = "p-2 category-item border-bottom";
      catDiv.style.cursor = "pointer";
      catDiv.textContent = `${cat.name}`;
      catDiv.dataset.categoryId = cat.id;

      catDiv.addEventListener("click", async () => {
        // Remove active class from all
        document.querySelectorAll(".category-item").forEach(el => el.classList.remove("active"));
        // Add active class to selected
        catDiv.classList.add("active");

        const response = await rpc("/product/list/by/category", {
          category_id: cat.id,
          search_term: searchInput?.value?.trim() || ""
        });
        const products = response.products;

        this.renderProductCards(products, cat);
      });

      categoryList.appendChild(catDiv);
    });

    // Auto-select the first category
    const firstParent = categories.find(cat => !cat.parent_id);
    const firstCategory = firstParent || categories[0];
    const firstCatElement = document.querySelector(`.category-item[data-category-id="${firstCategory.id}"]`);

    if (firstCatElement) {
      firstCatElement.classList.add("active");
      const response = await rpc("/product/list/by/category", {
        category_id: firstCategory.id,
        search_term: "",
      });
      this.renderProductCards(response.products, firstCategory);
    }

    // Search filter functionality
    if (searchInput) {
      searchInput.addEventListener("input", async (e) => {
        const searchTerm = e.target.value.trim();
        const selectedCategory = document.querySelector(".category-item.active");
        const categoryId = selectedCategory?.dataset?.categoryId;

        if (!categoryId) return;

        const response = await rpc("/product/list/by/category", {
          category_id: categoryId,
          search_term: searchTerm,
        });
        const products = response.products;

        this.renderProductCards(products, {
          id: categoryId,
          name: selectedCategory.textContent
        });
      });
    }
  }

  renderProductCards(products, cat) {
    const productList = document.querySelector("#product-list");
    const searchInput = document.querySelector("#product-search");
    const searchIcon = document.querySelector("#product-search1");
    const countDisplay = document.querySelector("#product-count");

    if (countDisplay) {
      countDisplay.innerHTML = `Total Products: <strong>${products.length}</strong>`;
      countDisplay.style.fontSize = "14px";
      countDisplay.style.display = "inline";
    }

    productList.innerHTML = `
    <div id="product-card-container">
      ${products.map(prod => `
        <div class="product-card" data-product-id="${prod.id}">
          <div class="card">
            <img src="${prod.image}" alt="${prod.name}">
            <div class="product-info">
              <h6>${prod.name}</h6>
              <div class="price">Rs. ${(prod.list_price || 0).toLocaleString("en-IN")}</div>
              <div class="product-type">${prod.pro_type || 'Machine'}</div>
            </div>
          </div>
        </div>
      `).join('')}
    </div>
    <div id="product-detail-view" class="mt-0" style="display:none;"></div>
  `;

    products.forEach(prod => {
      const card = productList.querySelector(`.product-card[data-product-id="${prod.id}"]`);
      if (card) {
        card.addEventListener("click", () => {
          const allCards = productList.querySelectorAll(".product-card");
          allCards.forEach(c => c.style.display = "none");

          const detailDiv = document.querySelector("#product-detail-view");
          detailDiv.innerHTML = `
  <div class="card shadow p-4 position-relative mt-0">
    <button id="back-to-list" class="btn btn-sm btn-secondary position-absolute" style="top: 10px; left: 10px; z-index: 10;">
      <i class="fa fa-arrow-left"></i>
    </button>
    <div class="row">
      <div class="col-md-4 text-center">
        <img src="${prod.image}" class="img-fluid rounded" id="main-product-image" style="max-height: 260px; cursor: zoom-in;"/>
   
      </div>
      <div class="col-md-8">
 <h2 class="fw-bold mb-2">${prod.name}</h2>
<p class="mb-2">
  <strong>Type :</strong> ${prod.pro_type || 'Machine'} &nbsp;&nbsp;
  <strong>Price :</strong> <span class="text-success">₹${prod.list_price || 0}</span>
</p>
<p class="mb-2"><strong>Category :</strong> ${cat.name}</p>
<div class="row mt-3 gx-2 gy-2">
  ${prod.image_1 ? `<div class="col-auto">
    <button class="modern-btn" id="show-images-btn">
      <img src="/vd_product_gallary/static/img/Images.svg" class="btn-icon me-1" alt="camera" /> Images
    </button>
  </div>` : ''}
  
  ${prod.video_url ? `<div class="col-auto">
    <button class="modern-btn" id="show-video-btn">
      <img src="/vd_product_gallary/static/img/Videos.svg" class="btn-icon me-1" alt="video" /> Video
    </button>
  </div>` : ''}
  
  ${prod.brochure_url ? `<div class="col-auto">
    <button class="modern-btn" id="show-brochure-btn">
      <img src="/vd_product_gallary/static/img/Brochures.svg" class="btn-icon me-1" alt="brochure" /> Brochure
    </button>
  </div>` : ''}

  <div class="col-auto">
    <button class="modern-btn btn-sm" id="send-whatsapp-btn"
      style="background-color: #25D366; color: white; border: none;">
      <img src="/vd_product_gallary/static/img/Whatsappp.svg" class="btn-icon me-1" alt="whatsapp" />
      WhatsApp
    </button>
  </div>

  <div class="col-auto">
    <button class="modern-btn yellow" id="add-history-btn">
      <img src="/vd_product_gallary/static/img/History.svg" class="btn-icon me-1" alt="add" /> Add History
    </button>
  </div>

  <div class="col-auto">
    <button class="modern-btn btn-outline-info" id="show-description-btn">
      <img src="/vd_product_gallary/static/img/Description.svg" class="btn-icon me-1" alt="description" />
      Description
    </button>
  </div>
</div>


      </div>
    </div>
    <div id="extra-product-content" class="row mt-3"></div>
  </div>`;

          detailDiv.style.display = "block";
          if (countDisplay) countDisplay.style.display = "none";
          document.querySelector("#category-list").style.display = "none";
          const productPanel = document.querySelector("#product-panel");
          productPanel.classList.remove("col-md-9");
          productPanel.classList.add("col-md-12");

          if (searchInput) searchInput.style.display = "none";
          if (searchIcon) searchIcon.style.display = "none";

          document.querySelector("#back-to-list").addEventListener("click", () => {
            allCards.forEach(c => c.style.display = "block");
            detailDiv.style.display = "none";

            document.querySelector("#category-list").style.display = "block";
            productPanel.classList.remove("col-md-12");
            productPanel.classList.add("col-md-9");

            if (searchInput) searchInput.style.display = "block";
            if (searchIcon) searchIcon.style.display = "inline";
            if (countDisplay) countDisplay.style.display = "inline";
          });

          const mainImage = document.getElementById("main-product-image");
          const lightbox = document.getElementById("image-lightbox");
          const zoomedImage = document.getElementById("zoomed-image");
          const closeBtn = document.getElementById("image-lightbox-close");

          if (mainImage && lightbox && zoomedImage && closeBtn) {
            mainImage.addEventListener("click", () => {
              zoomedImage.src = mainImage.src;
              lightbox.style.display = "flex";
            });

            closeBtn.addEventListener("click", () => {
              lightbox.style.display = "none";
            });

            lightbox.addEventListener("click", (e) => {
              if (e.target === lightbox) {
                lightbox.style.display = "none";
              }
            });
          }

          // Other buttons retain original functionality
          document.querySelector("#show-description-btn")?.addEventListener("click", () => {
  const descriptionHtml = `
    <div class="mt-3">
      <div class="p-2 bg-light rounded border">${prod.description || "No description available."}</div>
    </div>
  `;
  document.querySelector("#extra-product-content").innerHTML = descriptionHtml;
});
          document.querySelector("#show-images-btn")?.addEventListener("click", () => {
            const images = [prod.image_1, prod.image_2, prod.image_3, prod.image_4].filter(Boolean);
            const imageHtml = images.length > 0 ? `
            <div class="image-gallery mt-3">
              ${images.map(img => `
                <div>
                  <img src="${img}" class="img-fluid rounded bg-light" style="width: 100%; object-fit: contain;">
                </div>
              `).join('')}
            </div>` : "<p>No additional images available.</p>";
            document.querySelector("#extra-product-content").innerHTML = imageHtml;
          });

          document.querySelector("#show-video-btn")?.addEventListener("click", () => {
            const videoUrl = prod.video_url;
            document.querySelector("#extra-product-content").innerHTML = videoUrl
              ? `<div class="embed-responsive embed-responsive-16by9">
                <iframe class="embed-responsive-item w-100" height="600" src="${videoUrl}" allowfullscreen></iframe>
              </div>`
              : "<p>No video available.</p>";
          });

          document.querySelector("#show-brochure-btn")?.addEventListener("click", () => {
            const brochureUrl = prod.brochure_url;
            document.querySelector("#extra-product-content").innerHTML = brochureUrl
              ? `<iframe src="${brochureUrl}" width="100%" height="600" style="border: none;"></iframe>`
              : "<p>No brochure available.</p>";
          });

          document.querySelector("#add-history-btn")?.addEventListener("click", (e) => {
            this.customerHistory(e, prod);
          });

          document.querySelector("#send-whatsapp-btn")?.addEventListener("click", (e) => {
            this.sendWhatsAppWizard(e, prod, cat);
          });
          setTimeout(() => {
          const showImagesBtn = document.querySelector("#show-images-btn");
          if (showImagesBtn) {
            showImagesBtn.click();
          }
        }, 100);

        });
      }
    });
  }



  sendWhatsAppWizard(e, prod, cat) {
    e.stopPropagation();
    e.preventDefault();

    const message = `*Product Details*\nName: ${prod.name}\nPrice: ₹${prod.list_price || 0}\n\nYouTube Link: ${prod.video_url || 'N/A'}\n`;
    const options = {
      on_reverse_breadcrumb: this.on_reverse_breadcrumb,
    };

    this.action.doAction({
      name: "Send WhatsApp",
      type: 'ir.actions.act_window',
      res_model: 'whatsapp.wizard',
      view_mode: 'form',
      views: [[false, 'form']],
      target: 'new',
      context: {
        default_product_id: prod.id,
        default_message: message,
      },
    }, options);
  }

  customerHistory(e, prod) {
    e.stopPropagation();
    e.preventDefault();
    const options = {
      on_reverse_breadcrumb: this.on_reverse_breadcrumb,
    };

    this.action.doAction({
      name: "Add Customer History",
      type: 'ir.actions.act_window',
      res_model: 'product.history.wizard',
      view_mode: 'form',
      views: [[false, 'form']],
      target: 'new',
      context: {
        default_product_template_id: prod.id,
      },
    }, options);
  }

}
product_gallary_dashboard.template = "product_gallary_dashboard"
registry.category("actions").add("open_product_gallery_dashboard", product_gallary_dashboard)
