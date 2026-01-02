import React from 'react';
import ReactDOM from 'react-dom/client';
// Import CSS in correct order
import './index.css';
import './styles/main.css';
import './styles/base/reset.css';
import './styles/base/animations.css';
import './styles/components/header.css';
import './styles/components/cards.css';
import './styles/components/forms.css';
import './styles/components/buttons.css';
import './styles/components/badges.css';
import './styles/components/tables.css';
import './styles/components/alerts.css';
import './styles/components/loading.css';
import './styles/components/tabs.css';
import './styles/components/modal.css';
import './styles/utilities/layout.css';
import './styles/utilities/spacing.css';
import './styles/utilities/misc.css';
import './styles/utilities/responsive.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
