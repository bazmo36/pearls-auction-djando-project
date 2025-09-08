document.addEventListener('DOMContentLoaded', function () {
  const input = document.getElementById('id_amount');
  const increaseButton = document.getElementById('increase-bid-btn');
  const form = document.getElementById('bid-form');

  
  const minBid = parseInt(input.getAttribute('min')) || 0
  const step = parseInt(input.getAttribute('step')) || 1

  if (increaseButton && input && form) {
    
    if (!input.value) {
      input.value = minBid;
    }

    increaseButton.addEventListener('click', function () {
      let currentValue = parseInt(input.value) || minBid;
      input.value = currentValue + step;

     
      form.submit()
    })
  }
})
