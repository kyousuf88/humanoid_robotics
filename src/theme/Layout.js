import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatWidget from '@theme/ChatWidget';

function Layout(props) {
  return (
    <>
      <OriginalLayout {...props}>{props.children}</OriginalLayout>
      <ChatWidget />
    </>
  );
}

export default Layout;