import React from "react";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Home from "./pages/Home";
import './App.css';

// Using React.FC (Function Component) or a standard function is fine,
// but ensure the sub-components are also converted to .tsx
const App: React.FC = () => {
  return (
    <>
     < div className="app-layout">
      <Header />
      <main className="content">
        <Home />
      </main>
      <Footer />
    </div>
    </>
  );
}

export default App;