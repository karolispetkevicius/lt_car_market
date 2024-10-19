// pages/_app.js

import 'bootstrap/dist/css/bootstrap.min.css';  // Import Bootstrap CSS globally
import '../styles/globals.css';                 // Import your global styles (optional)

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />;
}

export default MyApp;