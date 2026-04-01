document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const body = document.body;
    const header = document.getElementById("siteHeader");
    const navToggle = document.getElementById("navToggle");
    const navPanel = document.getElementById("navPanel");
    const mainNav = document.getElementById("mainNav");
    const navLinks = mainNav ? Array.from(mainNav.querySelectorAll('a[href]')) : [];
    const leadForm = document.getElementById("leadForm");
    const revealNodes = Array.from(document.querySelectorAll(".reveal, .reveal-card"));
    const parallaxHeroes = Array.from(document.querySelectorAll("[data-parallax]"));
    const tiltNodes = Array.from(document.querySelectorAll(".js-tilt"));
    const galleryItems = Array.from(document.querySelectorAll("[data-gallery-item]"));
    const galleryModal = document.getElementById("galleryModal");
    const galleryModalImage = document.getElementById("galleryModalImage");
    const galleryModalTitle = document.getElementById("galleryModalTitle");
    const galleryModalCaption = document.getElementById("galleryModalCaption");
    const galleryCloseButtons = Array.from(document.querySelectorAll("[data-gallery-close]"));
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
    let lockedScrollY = 0;

    const clearContactHashFromUrl = () => {
        const isContactPage = window.location.pathname.replace(/\/+$/, "") === "/contacto";
        if (!isContactPage || window.location.hash !== "#contacto" || !window.history.replaceState) {
            return;
        }

        window.requestAnimationFrame(() => {
            window.history.replaceState(null, "", `${window.location.pathname}${window.location.search}`);
        });
    };

    const lockPageScroll = () => {
        lockedScrollY = window.scrollY || window.pageYOffset || 0;
        root.classList.add("scroll-lock");
        body.classList.add("scroll-lock");
        body.style.top = `-${lockedScrollY}px`;
    };

    const unlockPageScroll = () => {
        root.classList.remove("scroll-lock");
        body.classList.remove("scroll-lock");
        body.style.top = "";
        const previousScrollBehavior = root.style.scrollBehavior;
        root.style.scrollBehavior = "auto";
        window.scrollTo(0, lockedScrollY);
        window.requestAnimationFrame(() => {
            root.style.scrollBehavior = previousScrollBehavior;
        });
    };

    const openMenu = () => {
        if (!navToggle || !navPanel) {
            return;
        }

        navPanel.classList.add("is-open");
        navToggle.classList.add("is-open");
        navToggle.setAttribute("aria-expanded", "true");
        root.classList.add("nav-open");
        body.classList.add("nav-open");
    };

    const closeMenu = () => {
        if (!navToggle || !navPanel) {
            return;
        }

        const menuWasOpen = navPanel.classList.contains("is-open");
        if (!menuWasOpen) {
            return;
        }

        navPanel.classList.remove("is-open");
        navToggle.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
        root.classList.remove("nav-open");
        body.classList.remove("nav-open");
        if (!galleryModal || !galleryModal.classList.contains("is-open")) {
            unlockPageScroll();
        }
    };

    if (navToggle && navPanel && mainNav) {
        navToggle.addEventListener("click", () => {
            if (navPanel.classList.contains("is-open")) {
                closeMenu();
            } else {
                openMenu();
            }
        });

        navLinks.forEach((link) => {
            link.addEventListener("click", closeMenu);
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeMenu();
            }
        });

        document.addEventListener("click", (event) => {
            const clickedInsideNav = navPanel.contains(event.target);
            const clickedToggle = navToggle.contains(event.target);

            if (!clickedInsideNav && !clickedToggle) {
                closeMenu();
            }
        });

        window.addEventListener("resize", () => {
            if (window.innerWidth >= 768) {
                closeMenu();
            }
        });
    }

    const updateHeaderState = () => {
        if (!header) {
            return;
        }

        header.classList.toggle("is-scrolled", window.scrollY > 12);
    };

    const updateActiveNav = () => {
        const currentPath = window.location.pathname.replace(/\/+$/, "") || "/";

        navLinks.forEach((link) => {
            const href = link.getAttribute("href");
            if (!href || href.startsWith("http")) {
                return;
            }

            const linkPath = new URL(href, window.location.origin).pathname.replace(/\/+$/, "") || "/";
            link.classList.toggle("is-active", linkPath === currentPath);
        });
    };

    updateHeaderState();
    updateActiveNav();
    clearContactHashFromUrl();
    window.addEventListener("scroll", updateHeaderState, { passive: true });

    if (prefersReducedMotion) {
        revealNodes.forEach((node) => node.classList.add("is-visible"));
    } else if ("IntersectionObserver" in window) {
        const revealObserver = new IntersectionObserver(
            (entries, observer) => {
                entries.forEach((entry) => {
                    if (!entry.isIntersecting) {
                        return;
                    }

                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                });
            },
            {
                rootMargin: "0px 0px -12% 0px",
                threshold: 0.12,
            }
        );

        revealNodes.forEach((node) => revealObserver.observe(node));
    } else {
        revealNodes.forEach((node) => node.classList.add("is-visible"));
    }

    if (!prefersReducedMotion && parallaxHeroes.length) {
        let ticking = false;

        const updateParallax = () => {
            const viewportHeight = window.innerHeight || 1;

            parallaxHeroes.forEach((hero) => {
                const rect = hero.getBoundingClientRect();
                if (rect.bottom < 0 || rect.top > viewportHeight) {
                    hero.style.setProperty("--hero-shift", "0px");
                    return;
                }

                const progress = (rect.top + rect.height * 0.5 - viewportHeight * 0.5) / viewportHeight;
                const shift = Math.max(-14, Math.min(14, progress * -12));
                hero.style.setProperty("--hero-shift", `${shift}px`);
            });

            ticking = false;
        };

        const requestParallax = () => {
            if (ticking) {
                return;
            }

            ticking = true;
            window.requestAnimationFrame(updateParallax);
        };

        updateParallax();
        window.addEventListener("scroll", requestParallax, { passive: true });
        window.addEventListener("resize", requestParallax);
    }

    if (!prefersReducedMotion && canHover && tiltNodes.length) {
        tiltNodes.forEach((node) => {
            node.addEventListener("pointermove", (event) => {
                const rect = node.getBoundingClientRect();
                const px = (event.clientX - rect.left) / rect.width;
                const py = (event.clientY - rect.top) / rect.height;
                const rotateY = (px - 0.5) * 5;
                const rotateX = (0.5 - py) * 5;

                node.style.setProperty("--tilt-x", `${rotateX.toFixed(2)}deg`);
                node.style.setProperty("--tilt-y", `${rotateY.toFixed(2)}deg`);
                node.classList.add("is-hovered");
            });

            node.addEventListener("pointerleave", () => {
                node.style.setProperty("--tilt-x", "0deg");
                node.style.setProperty("--tilt-y", "0deg");
                node.classList.remove("is-hovered");
            });
        });
    }

    const openGallery = (item) => {
        if (!galleryModal || !galleryModalImage || !galleryModalTitle || !galleryModalCaption) {
            return;
        }

        galleryModalImage.src = item.dataset.gallerySrc || "";
        galleryModalImage.alt = item.querySelector("img")?.alt || "";
        galleryModalTitle.textContent = item.dataset.galleryTitle || "";
        galleryModalCaption.textContent = item.dataset.galleryCaption || "";
        galleryModal.classList.add("is-open");
        galleryModal.setAttribute("aria-hidden", "false");
        if (!body.classList.contains("scroll-lock")) {
            lockPageScroll();
        }
    };

    const closeGallery = () => {
        if (!galleryModal || !galleryModalImage) {
            return;
        }

        galleryModal.classList.remove("is-open");
        galleryModal.setAttribute("aria-hidden", "true");
        galleryModalImage.src = "";
        if (!navPanel || !navPanel.classList.contains("is-open")) {
            unlockPageScroll();
        }
    };

    if (galleryItems.length && galleryModal) {
        galleryItems.forEach((item) => {
            item.addEventListener("click", () => openGallery(item));
        });

        galleryCloseButtons.forEach((button) => {
            button.addEventListener("click", closeGallery);
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && galleryModal.classList.contains("is-open")) {
                closeGallery();
            }
        });
    }

    if (leadForm) {
        const formFields = {
            name: leadForm.querySelector("#name"),
            company: leadForm.querySelector("#company"),
            phone: leadForm.querySelector("#phone"),
            email: leadForm.querySelector("#email"),
            service: leadForm.querySelector("#service"),
            route: leadForm.querySelector("#route"),
            message: leadForm.querySelector("#message"),
        };
        const formStatus = document.getElementById("formStatus");

        const setFieldError = (fieldName, message = "") => {
            const field = formFields[fieldName];
            const errorNode = leadForm.querySelector(`[data-error-for="${fieldName}"]`);
            if (!field || !errorNode) {
                return;
            }

            errorNode.textContent = message;
            field.classList.toggle("is-invalid", Boolean(message));
            field.setAttribute("aria-invalid", message ? "true" : "false");
        };

        const clearAllFieldErrors = () => {
            Object.keys(formFields).forEach((fieldName) => setFieldError(fieldName, ""));
            if (formStatus) {
                formStatus.textContent = "";
                formStatus.className = "form-status";
            }
        };

        const validateName = (value) => {
            if (!value) {
                return "Ingresa tu nombre y apellido.";
            }

            if (value.length < 5 || value.trim().split(/\s+/).length < 2) {
                return "Escribe nombre y apellido completos.";
            }

            return "";
        };

        const validateCompany = (value) => {
            if (!value) {
                return "Ingresa el nombre de la empresa.";
            }

            if (value.length < 2) {
                return "El nombre de empresa es demasiado corto.";
            }

            return "";
        };

        const extractPhoneDigits = (value) => value.replace(/\D/g, "");

        const normalizePhone = (value) => {
            const digits = extractPhoneDigits(value);

            if (digits.startsWith("569") && digits.length === 11) {
                return `+${digits}`;
            }

            if (digits.startsWith("09") && digits.length === 10) {
                return `+56${digits.slice(1)}`;
            }

            if (digits.startsWith("9") && digits.length === 9) {
                return `+56${digits}`;
            }

            return value.replace(/\s+/g, "");
        };

        const formatPhoneForDisplay = (value) => {
            const normalized = normalizePhone(value);
            const digits = extractPhoneDigits(normalized);

            if (digits.startsWith("569") && digits.length === 11) {
                return `+56 9 ${digits.slice(3, 7)} ${digits.slice(7, 11)}`;
            }

            return value.trim();
        };

        const validatePhone = (value) => {
            if (!value) {
                return "Ingresa un teléfono de contacto.";
            }

            if (!/^\+569\d{8}$/.test(normalizePhone(value))) {
                return "Usa un celular chileno válido. Ejemplo: +56 9 1234 5678.";
            }

            return "";
        };

        const validateEmail = (value) => {
            if (!value) {
                return "Ingresa un correo de contacto.";
            }

            if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
                return "Ingresa un correo válido. Ejemplo: contacto@empresa.cl";
            }

            return "";
        };

        const validateService = (value) => {
            if (!value) {
                return "Selecciona el tipo de servicio.";
            }

            return "";
        };

        const validateRoute = (value) => {
            if (!value) {
                return "Indica la ruta o tramo del servicio.";
            }

            if (value.length < 5) {
                return "Especifica mejor la ruta. Ejemplo: Santiago - Antofagasta.";
            }

            if (!value.includes("-") && !/faena|puerto|bodega|origen|destino/i.test(value)) {
                return "Indica un origen y destino. Ejemplo: Santiago - Antofagasta.";
            }

            return "";
        };

        const validateMessage = (value) => {
            if (!value) {
                return "Describe brevemente tu requerimiento.";
            }

            if (value.length < 20) {
                return "Entrega más contexto: carga, urgencia, volumen o restricciones.";
            }

            return "";
        };

        const validators = {
            name: validateName,
            company: validateCompany,
            phone: validatePhone,
            email: validateEmail,
            service: validateService,
            route: validateRoute,
            message: validateMessage,
        };

        const validateField = (fieldName) => {
            const field = formFields[fieldName];
            if (!field) {
                return "";
            }

            const value = field.value.toString().trim();
            const error = validators[fieldName](value);
            setFieldError(fieldName, error);
            return error;
        };

        Object.entries(formFields).forEach(([fieldName, field]) => {
            if (!field) {
                return;
            }

            if (fieldName === "phone") {
                field.addEventListener("blur", () => {
                    field.value = formatPhoneForDisplay(field.value);
                    validateField(fieldName);
                });

                field.addEventListener("input", () => {
                    if (field.classList.contains("is-invalid")) {
                        validateField(fieldName);
                    }
                });

                return;
            }

            field.addEventListener("blur", () => {
                validateField(fieldName);
            });

            field.addEventListener("input", () => {
                if (field.classList.contains("is-invalid")) {
                    validateField(fieldName);
                }
            });
        });

        leadForm.addEventListener("submit", (event) => {
            event.preventDefault();
            clearAllFieldErrors();

            const formData = new FormData(leadForm);
            const whatsappNumber = leadForm.dataset.whatsappNumber;
            const fields = {
                name: formData.get("name")?.toString().trim(),
                company: formData.get("company")?.toString().trim(),
                phone: formData.get("phone")?.toString().trim(),
                email: formData.get("email")?.toString().trim(),
                service: formData.get("service")?.toString().trim(),
                route: formData.get("route")?.toString().trim(),
                message: formData.get("message")?.toString().trim(),
            };

            const errors = Object.keys(formFields)
                .map((fieldName) => validateField(fieldName))
                .filter(Boolean);

            if (errors.length || !whatsappNumber) {
                if (formStatus) {
                    formStatus.textContent = "Corrige los campos marcados para continuar.";
                    formStatus.className = "form-status is-error";
                }
                return;
            }

            const whatsappMessage = [
                "Hola, quiero solicitar una evaluacion logistica.",
                "",
                `Nombre: ${fields.name}`,
                `Empresa: ${fields.company}`,
                `Telefono: ${formatPhoneForDisplay(fields.phone)}`,
                `Correo: ${fields.email}`,
                `Servicio: ${fields.service}`,
                `Ruta: ${fields.route}`,
                `Detalle: ${fields.message}`,
            ].join("\n");

            const url = `https://wa.me/${whatsappNumber}?text=${encodeURIComponent(whatsappMessage)}`;
            window.open(url, "_blank", "noopener,noreferrer");
        });
    }
});
