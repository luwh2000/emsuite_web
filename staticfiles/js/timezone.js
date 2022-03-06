
// Small script for adding the client timezone to the cookie.

const tzName = Intl.DateTimeFormat().resolvedOptions().timeZone;
document.cookie = 'timezone=' + encodeURIComponent(tzName) + '; path=/; Secure';
