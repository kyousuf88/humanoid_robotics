import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

export default function Home() {
  return (
    <Layout title="Home" description="Description will go into a meta tag in <head />">
      <main style={{ padding: '4rem', textAlign: 'center' }}>
        <h1>Welcome to Humanoid Robotics</h1>
        <p>Your site is now running!</p>
        <div style={{ marginTop: '20px' }}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/intro">
            Get Started with Documentation ⏱️
          </Link>
        </div>
      </main>
    </Layout>
  );
}