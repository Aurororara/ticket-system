
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
  const form = document.getElementById('creditcardForm');
  if (form) {
    const cardNumberInput = document.getElementById('cardNumber');
    const submitButton = document.getElementById('submitPaymentBtn');
    const errorMsg = document.getElementById('errorMsg');
    const cardExpiryInput = document.getElementById('cardExpiry');

    // ➤ 輸入時自動每四位加一個空格
    if (cardNumberInput) {
      cardNumberInput.addEventListener('input', function (e) {
        let value = e.target.value.replace(/\D/g, ''); // 只保留數字
        if (value.length > 16) {
          value = value.slice(0, 16); // 最多16位數字
        }
        e.target.value = value.replace(/(.{4})/g, '$1 ').trim(); // 每4位加空格
      });
    }

    // ➤ 到期日輸入自動補 /
    if (cardExpiryInput) {
      cardExpiryInput.addEventListener('input', function (e) {
        let value = e.target.value.replace(/[^\d]/g, ''); // 僅保留數字
        if (value.length >= 3) {
          value = value.slice(0, 4);
          value = value.slice(0, 2) + '/' + value.slice(2);
        } else if (value.length >= 2) {
          value = value.slice(0, 2) + '/';
        }
        e.target.value = value;
      });

      // ➤ 按下 Backspace 自動移除 /
      cardExpiryInput.addEventListener('keydown', function (e) {
        const value = cardExpiryInput.value;
        if (e.key === 'Backspace' && value.length === 4 && value.charAt(2) === '/') {
          e.preventDefault();
          cardExpiryInput.value = value.slice(0, 2);
        }
      });
    }
    
  
    // ➤ 點擊「確認付款」按鈕事件
    document.getElementById('creditcardForm').addEventListener('submit', function (e) {
      e.preventDefault()
      const cardNumber = cardNumberInput.value.trim();
      const cardExpiry = cardExpiryInput.value.trim();
      const cardCVC = document.getElementById('cardCVC').value.trim();
      const orderIdInput = document.querySelector('input[name="order_id"]');
      const orderId = orderIdInput ? orderIdInput.value : null;
      let errorMessages = [];
      // ➤ 去除空格並驗證卡號為 16 位數字
      const rawCardNumber = cardNumber.replace(/\D/g, ''); // 移除所有非數字
      if (!/^\d{16}$/.test(rawCardNumber)) {
        errorMessages.push('卡號必須為16位數字');
      }

      // ➤ 檢查有效年月格式 MM/YY
      // ➤ 檢查有效年月格式 MM/YY
      if (!/^(0[1-9]|1[0-2])\/\d{2}$/.test(cardExpiry)) {
        errorMessages.push('有效年月格式錯誤，請使用MM/YY格式');
      } else {
        // ➤ 檢查是否過期
        const [expMonth, expYear] = cardExpiry.split('/').map(str => parseInt(str, 10));

        // ➤ 轉換成完整西元年
        const fullExpYear = expYear + 2000;

        const now = new Date();
        const thisMonth = now.getMonth() + 1; // getMonth() 是 0~11
        const thisYear = now.getFullYear();

        if (fullExpYear < thisYear || (fullExpYear === thisYear && expMonth < thisMonth)) {
          errorMessages.push('信用卡已過期，請輸入有效年月');
        }
      }

  
      // ➤ 檢查 CVC 為3位數字
      if (!/^\d{3}$/.test(cardCVC)) {
        errorMessages.push('安全碼必須為3位數字');
      }
  
      // ➤ 顯示錯誤或進行導向
      if (errorMessages.length > 0) {
        errorMsg.textContent = errorMessages.join('\n');
        errorMsg.classList.remove('d-none');
      } else {
        errorMsg.classList.add('d-none');
        form.submit();
      }
    })
  }
});

// 選擇票種
document.addEventListener('DOMContentLoaded', function () {
  const nextBtn = document.getElementById('typenextBtn');

  function updateButtonState() {
    const fullQtyEl = document.getElementById('hiddenFullTicketQty');
    const disabledQtyEl = document.getElementById('hiddenDisabledTicketQty');

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

      const max = parseInt(qtyInput.dataset.max || "0");
      let qty = parseInt(qtyInput.value);

      if (action === "increase" && qty < max) {
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
  const phoneInput = document.getElementById('contact_phone');
  if (phoneInput) {
    phoneInput.addEventListener('input', function (e) {
      let value = e.target.value.replace(/\D/g, ''); // 只保留數字
      if (value.length > 10) {
        value = value.slice(0, 10); // 最多10位
      }
      e.target.value = value;
    });
  }

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
