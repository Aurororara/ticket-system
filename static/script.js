
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
      errorMsg.classList.remove('d-none');

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
    errorMsg.classList.add('d-none');
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

// 信用卡確認付款模擬 跳轉
document.addEventListener('DOMContentLoaded', function () {
  const submitButton = document.getElementById('submitPaymentBtn');
  if (submitButton) {
    submitButton.addEventListener('click', function () {

      const cardNumber = document.getElementById('cardNumber').value.trim();
      const cardExpiry = document.getElementById('cardExpiry').value.trim();
      const cardCVC = document.getElementById('cardCVC').value.trim();
      const errorMsg = document.getElementById('errorMsg');
      
      const orderIdInput = document.querySelector('input[name="order_id"]');
      const orderId = orderIdInput ? orderIdInput.value : null;


      let errorMessages = [];

      phoneInput.addEventListener('input', function () {
        this.value = this.value.replace(/\D/g, ''); // 移除非數字字元
      });

      // 檢查卡號 16 位數字
      if (!/^\d{16}$/.test(cardNumber)) {
        errorMessages.push('卡號必須為16位數字');
      }

      // 檢查有效年月 MM/YY 格式
      if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(cardExpiry)) {
        errorMessages.push('有效年月格式錯誤，請使用MM/YY格式');
      }

      // 檢查 CVC 3 位數字
      if (!/^\d{3}$/.test(cardCVC)) {
        errorMessages.push('安全碼必須為3位數字');
      }

      if (errorMessages.length > 0) {
        errorMsg.textContent = errorMessages.join('\n');
        errorMsg.classList.remove('d-none');
      } else {
        errorMsg.classList.add('d-none');
        // 驗證成功後，跳轉到帶 order_id 的完成頁
        if (orderId) {
          window.location.href = '/ticket/order-complete/' + orderId;
        } else {
          console.error('無法取得 order_id');
        }
      }
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

// atm資料確認
if (document.getElementById('paymentForm')) {
  document.getElementById('paymentForm').addEventListener('submit', function (e) {
    const name = document.getElementById('contact_name').value.trim();
    const email = document.getElementById('contact_email').value.trim();
    const phone = document.getElementById('contact_phone').value.trim();
    const errorMessage = document.getElementById('errorMessage');

    let missingFields = [];
    if (!name) missingFields.push('姓名');
    if (!email) missingFields.push('Email');
    if (!phone) {
      missingFields.push('手機');
    } else if (!/^09\d{8}$/.test(phone)) {  // 檢查手機格式
      missingFields.push('手機號碼格式錯誤，請輸入09開頭共10位數字');
    }
    if (missingFields.length > 0) {
      e.preventDefault();
      errorMessage.textContent = '請填寫以下欄位：' + missingFields.join('、');
      errorMessage.classList.remove('d-none');
    } else {
      errorMessage.classList.add('d-none');

      const orderId = document.querySelector('input[name="order_id"]').value;
      window.location.href = '/ticket/order-complete/' + orderId;
      
    }
  });
}

//email是否註冊過
document.addEventListener('DOMContentLoaded', function () {
  const emailInput = document.getElementById('email');
  const emailExistMsg = document.getElementById('emailExist');

  emailInput.addEventListener('blur', function () {
    const emailVal = emailInput.value.trim();
    if (!emailVal) {
      emailExistMsg.style.display = 'none';
      return;
    }

    fetch(`/check_email?email=${encodeURIComponent(emailVal)}`)
      .then(response => response.json())
      .then(data => {
        if (data.exists) {
          emailExistMsg.style.display = 'block';
        } else {
          emailExistMsg.style.display = 'none';
        }
      });
  });
});

// 即時檢查電話是否存在
const phoneInput = document.getElementById('phone');
const phoneExistMsg = document.getElementById('phoneExist');

phoneInput.addEventListener('blur', function () {
  const phoneVal = phoneInput.value.trim();
  if (!phoneVal) {
    phoneExistMsg.style.display = 'none';
    return;
  }

  fetch(`/check_exist?phone=${encodeURIComponent(phoneVal)}`)
    .then(response => response.json())
    .then(data => {
      phoneExistMsg.style.display = data.exists ? 'block' : 'none';
    });
});

// 限制只能輸入數字
phoneInput.addEventListener('input', function () {
  this.value = this.value.replace(/\D/g, '');
});
