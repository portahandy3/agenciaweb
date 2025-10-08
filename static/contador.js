document.addEventListener("DOMContentLoaded", () => {
  const counters = document.querySelectorAll('.counter');

  counters.forEach(counter => {
    const target = +counter.getAttribute('data-target');
    let current = 0;

    const updateCounter = () => {
      const increment = target / 100;

      if (current < target) {
        current += increment;
        counter.innerText = `${Math.ceil(current)}`;
        setTimeout(updateCounter, 20);
      } else {
        counter.innerText = target;
      }
    };

    updateCounter();
  });
});

