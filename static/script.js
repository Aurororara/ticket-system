
// 選擇區域下一步 按鈕
document.addEventListener('DOMContentLoaded', function () {
  const agreeCheckbox = document.getElementById('agreeTerms');
  const nextButton = document.getElementById('areaNextBtn');
  const errorMsg = document.getElementById('errorMsg');
  const areaForm = document.getElementById('areaForm');

  nextButton.addEventListener('click', function (event) {
    const selectedAreaInput = document.querySelector('input[name="selected_area"]:checked');
    const isAreaSelected = selectedAreaInput !== null;
    const isTermsChecked = agreeCheckbox.checked;

    if (!isAreaSelected || !isTermsChecked) {
      event.preventDefault();  // 阻止預設行為
      errorMsg.style.display = 'block';

      if (!isAreaSelected && !isTermsChecked) {
        errorMsg.textContent = '請選擇一個區域並同意服務條款與隱私權政策';
      } else if (!isAreaSelected) {
        errorMsg.textContent = '請選擇一個區域';
      } else if (!isTermsChecked) {
        errorMsg.textContent = '請同意服務條款與隱私權政策';
      }
      return;
    }

    // 驗證成功，取得區域與場次 ID 進行跳轉
    errorMsg.style.display = 'none';
    const areaId = selectedAreaInput.value;
    const gameId = areaForm.dataset.gameId;
    window.location.href = `/ticket/${gameId}/${areaId}/select-type`;
  });
});



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
    const fullQtyEl = document.getElementById('fullTicketQty');
    const disabledQtyEl = document.getElementById('disabledTicketQty');

    if (!fullQtyEl || !disabledQtyEl) return;

    const totalQty = parseInt(fullQtyEl.value) + parseInt(disabledQtyEl.value);
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
});
