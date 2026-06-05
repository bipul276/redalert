export default function PrivacyPolicy() {
    return (
        <div className="max-w-3xl mx-auto space-y-8 py-8 px-4">
            <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">Privacy Policy</h1>
            <p className="text-sm text-muted-foreground">Last updated: {new Date().toLocaleDateString()}</p>
            
            <div className="space-y-6 text-foreground/90 leading-relaxed">
                <section>
                    <h2 className="text-2xl font-semibold mb-3">1. Introduction</h2>
                    <p>
                        Welcome to RedAlert. We believe in transparency and data minimization. As a public safety aggregator, our goal is to provide you with critical information without compromising your privacy.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">2. What We Don't Collect</h2>
                    <p>
                        RedAlert is designed to be used openly. We do <strong>not</strong> require public user accounts, nor do we collect personal identifiers such as your name, email address, phone number, or physical address.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">3. Analytics, Advertising, and Cookies</h2>
                    <p className="mb-2">
                        To help us improve the platform and keep it free to use, we utilize standard analytics and advertising tools (such as Google Analytics and Google AdSense). These tools may collect anonymous, aggregated usage data, including:
                    </p>
                    <ul className="list-disc pl-6 space-y-2 mb-4">
                        <li>General geographic location (e.g., country or city level).</li>
                        <li>Browser type and operating system.</li>
                        <li>Pages visited and time spent on the platform.</li>
                    </ul>
                    
                    <h3 className="text-xl font-medium mt-4 mb-2 text-foreground">Google Ads & Cookies</h3>
                    <ul className="list-disc pl-6 space-y-2">
                        <li>Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites.</li>
                        <li>Google's use of advertising cookies enables it and its partners to serve ads to users based on their visit to our site and/or other sites on the Internet.</li>
                        <li>Users may opt out of personalized advertising by visiting <a href="https://myadcenter.google.com/" target="_blank" rel="noopener noreferrer" className="text-primary hover:underline">Google Ads Settings</a>.</li>
                    </ul>
                    <p className="mt-4">
                        You can also adjust your browser settings to block all cookies if you prefer, though this may affect site functionality.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">4. Third-Party Data Collection</h2>
                    <p>
                        We <strong>do not</strong> sell, rent, or trade your data directly to third parties. However, as noted above, third-party advertising networks (like Google) may independently collect anonymous usage data through cookies to serve targeted advertisements.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">5. Contact Us</h2>
                    <p>
                        If you have any questions or concerns about our privacy practices, please contact us at: <a href="mailto:bipulnandan276@gmail.com" className="text-primary hover:underline">bipulnandan276@gmail.com</a>
                    </p>
                </section>
            </div>
        </div>
    );
}
