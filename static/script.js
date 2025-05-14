

// 選擇區域下一步 按鈕
document.addEventListener('DOMContentLoaded', function () {
  function setupQuantityControl(minusBtn, plusBtn, qtyInput, hiddenInput) {
    minusBtn.addEventListener('click', function (event) {
      event.preventDefault();
      let qty = parseInt(qtyInput.value);
      if (qty > 0) qtyInput.value = qty - 1;
      hiddenInput.value = qtyInput.value;
      toggleNextButton();
    });

    plusBtn.addEventListener('click', function (event) {
      event.preventDefault();
      let qty = parseInt(qtyInput.value);
      qtyInput.value = qty + 1;
      hiddenInput.value = qtyInput.value;
      toggleNextButton();
    });
  }

  function toggleNextButton() {
    const totalQty = parseInt(fullTicketQty.value) + parseInt(disabledTicketQty.value);
    const nextBtn = document.getElementById('typenextBtn');
    nextBtn.disabled = totalQty <= 0;
  }

  const fullTicketMinus = document.querySelectorAll('.minus')[0];
  const fullTicketPlus = document.querySelectorAll('.plus')[0];
  const fullTicketQty = document.getElementById('fullTicketQty');
  const hiddenFullTicketQty = document.getElementById('hiddenFullTicketQty');

  const disabledTicketMinus = document.querySelectorAll('.minus')[1];
  const disabledTicketPlus = document.querySelectorAll('.plus')[1];
  const disabledTicketQty = document.getElementById('disabledTicketQty');
  const hiddenDisabledTicketQty = document.getElementById('hiddenDisabledTicketQty');

  setupQuantityControl(fullTicketMinus, fullTicketPlus, fullTicketQty, hiddenFullTicketQty);
  setupQuantityControl(disabledTicketMinus, disabledTicketPlus, disabledTicketQty, hiddenDisabledTicketQty);

  toggleNextButton();
});

// 啟用或停用 下一步 按鈕
document.addEventListener('DOMContentLoaded', function () {
  const agreeCheckbox = document.getElementById('agreeTerms');
  const nextButton = document.getElementById('nextBtn');


// 付款方式說明切換
document.querySelectorAll('input[name="payment"]').forEach(radio => {
  radio.addEventListener('change', function () {
    const description = document.getElementById('paymentDescription');
    if (this.id === 'creditCard') {
      description.innerHTML = `
        <strong>信用卡付款（Credit Card）</strong>
        <ol>
          <li>僅限 VISA, Mastercard, JCB。</li>
          <li>未能正常扣款請聯絡發卡銀行。</li>
        </ol>`;
    } else if (this.id === 'atmTransfer') {
      description.innerHTML = `
        <strong>ATM 付款（ATM Fund Transfer）</strong>
        <ol>
          <li>請於 5 日內完成付款，並保存收據。</li>
          <li>未按時付款訂單將自動取消。</li>
        </ol>`;
    }
  });
});

// 確認付款模擬跳轉
document.addEventListener('DOMContentLoaded', function () {
  const submitButton = document.getElementById('submitPaymentBtn');
  if (submitButton) {
    submitButton.addEventListener('click', function () {
      alert('付款成功，感謝您的訂購！');
      window.location.href = '/payment/success'; // 替換為你的完成頁面路由
    });
  }
});

// 選擇票種
document.addEventListener('DOMContentLoaded', function () {
  const nextBtn = document.getElementById('typenextBtn');

  function updateButtonState() {
    const totalQty = parseInt(document.getElementById('fullTicketQty').value) + parseInt(document.getElementById('disabledTicketQty').value);
    nextBtn.disabled = totalQty <= 0;
  }

  document.querySelectorAll('.quantity-btn').forEach(btn => {
    btn.addEventListener('click', function () {
      const targetId = this.dataset.target;
      const hiddenId = this.dataset.hidden;
      const action = this.dataset.action;

      const qtyInput = document.getElementById(targetId);
      const hiddenInput = document.getElementById(hiddenId);

      let qty = parseInt(qtyInput.value);

      if (action === 'increase') {
        qty += 1;
      } else if (action === 'decrease' && qty > 0) {
        qty -= 1;
      }

      qtyInput.value = qty;
      hiddenInput.value = qty;
      updateButtonState();
    });
  });

  updateButtonState();
})})
