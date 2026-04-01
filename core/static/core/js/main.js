document.addEventListener("DOMContentLoaded", () => {
    const root = document.documentElement;
    const body = document.body;
    const header = document.getElementById("siteHeader");
    const navToggle = document.getElementById("navToggle");
    const navPanel = document.getElementById("navPanel");
    const mainNav = document.getElementById("mainNav");
    const navLinks = mainNav ? Array.from(mainNav.querySelectorAll('a[href]')) : [];
    const revealNodes = Array.from(document.querySelectorAll(".reveal, .reveal-card"));
    const parallaxHeroes = Array.from(document.querySelectorAll("[data-parallax]"));
    const tiltNodes = Array.from(document.querySelectorAll(".js-tilt"));
    const galleryItems = Array.from(document.querySelectorAll("[data-gallery-item]"));
    const galleryModal = document.getElementById("galleryModal");
    const galleryModalImage = document.getElementById("galleryModalImage");
    const galleryModalTitle = document.getElementById("galleryModalTitle");
    const galleryModalCaption = document.getElementById("galleryModalCaption");
    const galleryCloseButtons = Array.from(document.querySelectorAll("[data-gallery-close]"));
    const formToastStack = document.querySelector(".form-toast-stack");
    const leadForm = document.getElementById("leadForm");
    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const canHover = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
    let lockedScrollY = 0;
    let scrollIsLocked = false;
    let lastGalleryTrigger = null;

    if (galleryModal) {
        galleryModal.inert = true;
    }

    const clearContactHashFromUrl = () => {
        const isContactPage = window.location.pathname.replace(/\/+$/, "") === "/contacto";
        if (!isContactPage || window.location.hash !== "#contacto" || !window.history.replaceState) {
            return;
        }

        const contactSection = document.getElementById("contacto");
        if (!contactSection) {
            return;
        }

        window.setTimeout(() => {
            contactSection.scrollIntoView({
                block: "start",
                behavior: "auto",
            });

            window.requestAnimationFrame(() => {
                window.history.replaceState(null, "", `${window.location.pathname}${window.location.search}`);
            });
        }, 80);
    };

    const lockPageScroll = () => {
        if (scrollIsLocked) {
            return;
        }

        lockedScrollY = window.scrollY || window.pageYOffset || 0;
        root.classList.add("scroll-lock");
        body.classList.add("scroll-lock");
        body.style.top = `-${lockedScrollY}px`;
        scrollIsLocked = true;
    };

    const unlockPageScroll = () => {
        if (!scrollIsLocked) {
            return;
        }

        root.classList.remove("scroll-lock");
        body.classList.remove("scroll-lock");
        body.style.top = "";
        const previousScrollBehavior = root.style.scrollBehavior;
        root.style.scrollBehavior = "auto";
        window.scrollTo(0, lockedScrollY);
        window.requestAnimationFrame(() => {
            root.style.scrollBehavior = previousScrollBehavior;
        });
        scrollIsLocked = false;
    };

    const syncScrollLock = () => {
        const shouldLock = galleryModal && galleryModal.classList.contains("is-open");

        if (shouldLock) {
            lockPageScroll();
            return;
        }

        unlockPageScroll();
    };

    const openMenu = () => {
        if (!navToggle || !navPanel) {
            return;
        }

        navPanel.classList.add("is-open");
        navToggle.classList.add("is-open");
        navToggle.setAttribute("aria-expanded", "true");
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

    if (formToastStack) {
        window.setTimeout(() => {
            formToastStack.remove();
        }, 6000);
    }

    if (leadForm) {
        const serviceOptions = new Set([
            "Transporte nacional e internacional",
            "Logística minera",
            "Asesoría en comercio exterior",
            "Cargas especiales",
            "Cargas refrigeradas",
            "Carga peligrosa",
            "Sobredimensión",
            "Proyecto logístico",
        ]);
        const fieldRules = {
            nombre: {
                element: leadForm.querySelector('[name="nombre"]'),
                validate(value) {
                    const normalized = value.trim().replace(/\s+/g, " ");
                    if (!normalized) {
                        return "Ingresa tu nombre y apellido.";
                    }
                    if (normalized.length < 5 || normalized.split(" ").length < 2) {
                        return "Escribe nombre y apellido completos.";
                    }
                    return "";
                },
            },
            empresa: {
                element: leadForm.querySelector('[name="empresa"]'),
                validate(value) {
                    const normalized = value.trim();
                    if (!normalized) {
                        return "Ingresa el nombre de la empresa.";
                    }
                    if (normalized.length < 2) {
                        return "El nombre de la empresa es demasiado corto.";
                    }
                    return "";
                },
            },
            telefono: {
                element: leadForm.querySelector('[name="telefono"]'),
                validate(value) {
                    const normalized = value.trim();
                    if (!normalized) {
                        return "Ingresa un teléfono de contacto.";
                    }
                    if (/[A-Za-zÁÉÍÓÚáéíóúÑñ]/.test(normalized)) {
                        return "El teléfono solo puede contener números, espacios, paréntesis, + o guiones.";
                    }
                    const digits = normalized.replace(/\D/g, "");
                    if (!digits) {
                        return "Ingresa un teléfono válido. Ejemplo: +56 9 1234 5678.";
                    }
                    let formatted = normalized;
                    if (digits.startsWith("569") && digits.length === 11) {
                        formatted = `+${digits}`;
                    } else if (digits.startsWith("09") && digits.length === 10) {
                        formatted = `+56${digits.slice(1)}`;
                    } else if (digits.startsWith("9") && digits.length === 9) {
                        formatted = `+56${digits}`;
                    }
                    if (formatted !== normalized) {
                        this.element.value = formatted;
                    }
                    const formattedDigits = formatted.replace(/\D/g, "");
                    if (formattedDigits.length !== 11 || !formattedDigits.startsWith("569")) {
                        return "Usa un celular chileno válido. Ejemplo: +56 9 1234 5678.";
                    }
                    return "";
                },
            },
            email: {
                element: leadForm.querySelector('[name="email"]'),
                validate(value) {
                    const normalized = value.trim();
                    if (!normalized) {
                        return "Ingresa un correo de contacto.";
                    }
                    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailPattern.test(normalized)) {
                        return "Ingresa un correo válido. Ejemplo: contacto@empresa.cl.";
                    }
                    return "";
                },
            },
            servicio: {
                element: leadForm.querySelector('[name="servicio"]'),
                validate(value) {
                    const normalized = value.trim();
                    if (!normalized) {
                        return "Selecciona un servicio.";
                    }
                    if (!serviceOptions.has(normalized)) {
                        return "Selecciona una opción válida de servicio.";
                    }
                    return "";
                },
            },
            mensaje: {
                element: leadForm.querySelector('[name="mensaje"]'),
                validate(value) {
                    const normalized = value.trim();
                    if (!normalized) {
                        return "Describe tu requerimiento.";
                    }
                    if (normalized.length < 20) {
                        return "Entrega más contexto: carga, urgencia, volumen o restricciones.";
                    }
                    return "";
                },
            },
        };

        const setFieldError = (fieldName, message) => {
            const rule = fieldRules[fieldName];
            if (!rule?.element) {
                return;
            }

            const errorNode = leadForm.querySelector(`[data-error-for="${fieldName}"]`);
            const hasError = Boolean(message);
            rule.element.classList.toggle("is-invalid", hasError);
            rule.element.setAttribute("aria-invalid", hasError ? "true" : "false");

            if (errorNode) {
                errorNode.textContent = message || "";
            }
        };

        const validateField = (fieldName) => {
            const rule = fieldRules[fieldName];
            if (!rule?.element) {
                return "";
            }

            const message = rule.validate(rule.element.value);
            setFieldError(fieldName, message);
            return message;
        };

        const focusFirstInvalidField = () => {
            const invalidField = leadForm.querySelector(".is-invalid");
            if (!invalidField) {
                return;
            }

            invalidField.focus({ preventScroll: true });
            invalidField.scrollIntoView({
                behavior: prefersReducedMotion ? "auto" : "smooth",
                block: "center",
            });
        };

        Object.entries(fieldRules).forEach(([fieldName, rule]) => {
            if (!rule.element) {
                return;
            }

            const eventName = rule.element.tagName === "SELECT" ? "change" : "input";
            rule.element.addEventListener(eventName, () => {
                if (fieldName === "telefono") {
                    const sanitizedValue = rule.element.value.replace(/[^0-9+\s()-]/g, "");
                    if (sanitizedValue !== rule.element.value) {
                        rule.element.value = sanitizedValue;
                    }
                }

                if (rule.element.classList.contains("is-invalid")) {
                    validateField(fieldName);
                }
            });

            rule.element.addEventListener("blur", () => {
                validateField(fieldName);
            });
        });

        leadForm.addEventListener("submit", (event) => {
            let firstInvalidField = null;

            Object.keys(fieldRules).forEach((fieldName) => {
                const message = validateField(fieldName);
                if (!firstInvalidField && message) {
                    firstInvalidField = fieldRules[fieldName].element;
                }
            });

            if (!firstInvalidField) {
                return;
            }

            event.preventDefault();
            firstInvalidField.focus({ preventScroll: true });
            firstInvalidField.scrollIntoView({
                behavior: prefersReducedMotion ? "auto" : "smooth",
                block: "center",
            });
        });

        const shouldFocusServerErrors = leadForm.dataset.focusOnError === "true" || Boolean(leadForm.querySelector(".is-invalid"));
        if (shouldFocusServerErrors) {
            window.setTimeout(() => {
                leadForm.scrollIntoView({
                    behavior: prefersReducedMotion ? "auto" : "smooth",
                    block: "start",
                });
                focusFirstInvalidField();
            }, 120);
        }
    }

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
        lastGalleryTrigger = item;
        galleryModal.inert = false;
        galleryModal.classList.add("is-open");
        galleryModal.setAttribute("aria-hidden", "false");
        syncScrollLock();
    };

    const closeGallery = () => {
        if (!galleryModal || !galleryModalImage) {
            return;
        }

        if (document.activeElement instanceof HTMLElement && galleryModal.contains(document.activeElement)) {
            document.activeElement.blur();
        }

        galleryModal.classList.remove("is-open");
        galleryModal.inert = true;
        galleryModal.setAttribute("aria-hidden", "true");
        galleryModalImage.src = "";
        syncScrollLock();

        if (lastGalleryTrigger instanceof HTMLElement) {
            lastGalleryTrigger.focus({ preventScroll: true });
        }

        lastGalleryTrigger = null;
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

});
