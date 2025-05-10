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
