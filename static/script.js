function showTab(tabName) {
  const tabContent = document.getElementById('tabContent');
  let content = '';

  switch (tabName) {
    case 'intro':
      content = '這裡是節目介紹內容。';
      break;
    case 'notice':
      content = '這裡是注意事項內容。';
      break;
    case 'seats':
      content = '這裡是票區座位內容。';
      break;
    case 'pickup':
      content = '這裡是取票說明內容。';
      break;
    case 'map':
      content = '這裡是場館說明內容。';
      break;
    default:
      content = '請選擇上方任一按鈕以檢視相關資訊。';
  }

  tabContent.innerHTML = `<p>${content}</p>`;

  // Update button states
  document.querySelectorAll('.btn-group .btn').forEach(btn => btn.classList.remove('active'));
  const buttons = {
    'intro': 0,
    'notice': 1,
    'seats': 2,
    'pickup': 3,
    'map': 4
  };
  document.querySelectorAll('.btn-group .btn')[buttons[tabName]].classList.add('active');
}


// 選擇區域下一步 按鈕
document.addEventListener('DOMContentLoaded', function () {
  const agreeCheckbox = document.getElementById('agreeTerms');
  const nextButton = document.getElementById('areaNextBtn');
  const errorMsg = document.getElementById('errorMsg');
  const areaForm = document.getElementById('areaForm');

  areaForm.addEventListener('submit', function (event) {
    const isAreaSelected = document.querySelector('input[name="selected_area"]:checked') !== null;
    const isTermsChecked = agreeCheckbox.checked;

    // 檢查兩個條件是否都符合
    if (!isAreaSelected || !isTermsChecked) {
      event.preventDefault();  // 阻止表單送出
      errorMsg.style.display = 'block';

      if (!isAreaSelected && !isTermsChecked) {
        errorMsg.textContent = '請選擇一個區域並同意服務條款與隱私權政策';
      } else if (!isAreaSelected) {
        errorMsg.textContent = '請選擇一個區域';
      } else if (!isTermsChecked) {
        errorMsg.textContent = '請同意服務條款與隱私權政策';
      }
    } else {
      errorMsg.style.display = 'none';  // 通過驗證則隱藏錯誤訊息
    }
  });
});

// 啟用或停用 下一步 按鈕
document.addEventListener('DOMContentLoaded', function () {
  const agreeCheckbox = document.getElementById('agreeTerms');
  const nextButton = document.getElementById('nextBtn');

  if (agreeCheckbox && nextButton) {
    agreeCheckbox.addEventListener('change', function () {
      nextButton.disabled = !this.checked;
    });
  }
});

// 控制票數增減
document.querySelectorAll('.input-group').forEach(group => {
  const minusBtn = group.querySelector('.minus');
  const plusBtn = group.querySelector('.plus');
  const quantityInput = group.querySelector('.quantity');

  minusBtn.addEventListener('click', () => {
    let val = parseInt(quantityInput.value);
    if (val > 0) quantityInput.value = val - 1;
  });

  plusBtn.addEventListener('click', () => {
    let val = parseInt(quantityInput.value);
    quantityInput.value = val + 1;
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


