function autoFillSample(type) {
  const area = document.getElementById('content');
  if (!area) return;

  if (type === 'url') {
    area.value = 'http://secure-login-paypal-update.verify-user-account.ru';
  } else {
    area.value = 'Dear customer, your account has been suspended due to unusual activity. Verify your password and OTP immediately using this secure link: http://account-check-security.info';
  }
}

function fillSafeSample() {
  const type = document.getElementById('input_type');
  const area = document.getElementById('content');
  if (!type || !area) return;

  if (type.value === 'url') {
    area.value = 'https://github.com';
  } else {
    area.value = 'Hi team, please join the project review meeting tomorrow at 3 PM and share your status updates.';
  }
}
