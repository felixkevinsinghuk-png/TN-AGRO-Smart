const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
  container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
  container.classList.remove("right-panel-active");
});

async function sendOTP() {
  const email = document.getElementById("Email").value;
  const name = document.getElementById("Name").value;

  const res = await fetch("/send-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, name })
  });

  const data = await res.json();
  document.getElementById("signup-status").innerText = data.message;
  if (data.success) {
    document.getElementById("otpSection").style.display = "block";
  }
}

async function verifyOTP() {
  const email = document.getElementById("Email").value;
  const otp = document.getElementById("OTP").value;

  const res = await fetch("/verify-otp", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, otp })
  });

  const data = await res.json();
  document.getElementById("signup-status").innerText = data.message;
  if (data.success) {
    alert("Signup successful!");
  }
}

async function signinOTP() {
  const mobileNumber = document.getElementById("mobile number ").value.trim();
  const otp = document.getElementById("otpSignIn").value.trim();

  // Example logic to verify OTP (you may replace it with actual backend validation)
  if (mobileNumber === "9234567890" && otp === "3729") {
    // Redirect after successful OTP verification
    window.location.href = "http://127.0.0.1:5000";
  } else {
    alert("Invalid Mobile Number or OTP. Please try again.");
  }
}
