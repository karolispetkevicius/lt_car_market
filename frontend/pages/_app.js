// src/pages/_app.js
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS globally
import '../styles/globals.css'; // Import your global styles
import Layout from '../components/Layout'; // Make sure this path is correct

function MyApp({ Component, pageProps }) {
  return (
    <Layout>
      <Component {...pageProps} />
    </Layout>
  );
}

export default MyApp;