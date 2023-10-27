
var swiper = new Swiper(".mySwiper", {
    slidesPerView: 3,
    spaceBetween: 30,
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
    breakpoints: {
      300: {
        slidesPerView: 1.5,
        spaceBetween: 30,
        centeredSlides: true,
        initialSlide: 1,
      },
        400: {
            slidesPerView: 1.5,
            spaceBetween: 30,
            centeredSlides: true,
            initialSlide: 1,
          },
        620: {
            slidesPerView: 2,
            spaceBetween: 30,
            centeredSlides: true,
            initialSlide: 1,
          },
        800: {
            slidesPerView: 2,
            spaceBetween: 30,
            centeredSlides: true,
            initialSlide: 1,
          },
        940: {
            slidesPerView: 3,
            centeredSlides: true,
            spaceBetween: 30,
            initialSlide: 1,
          },
        1168: {
          slidesPerView: 3,
          spaceBetween: 30
        }
      }
  });
