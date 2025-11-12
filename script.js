// Set current year in footer
document.addEventListener("DOMContentLoaded", function () {
  const yearSpan = document.getElementById("year");
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  // Make all "Notify Me" buttons open an email to support@momaiverse.com
  const notifyButtons = document.querySelectorAll(".notify-btn");
  notifyButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const subject = btn.getAttribute("data-subject") || "Notify me";
      const body = [
        "Hi MomAIverse,",
        "",
        "I’d like to be notified when this is live:",
        subject,
        "",
        "My name:",
        "My best email:",
        "",
        "(You can remove anything you don’t want to share.)"
      ].join("%0D%0A");

      const mailtoLink = `mailto:support@momaiverse.com?subject=${encodeURIComponent(
        subject
      )}&body=${body}`;

      window.location.href = mailtoLink;
    });
  });
});
// Stripe Checkout Redirect
async function startCheckout() {
  try {
    const response = await fetch("https://momaiverse-server.onrender.com/create-checkout-session", {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    const data = await response.json();

    if (data.url) {
      window.location.href = data.url;  // Redirect to Stripe Checkout
    } else {
      alert("Could not start checkout — missing Stripe URL.");
    }

  } catch (error) {
    console.error("Checkout error:", error);
    alert("Connection error — please refresh and try again.");
  }
}
