export default function TermsOfService() {
    return (
        <div className="max-w-3xl mx-auto space-y-8 py-8 px-4">
            <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">Terms of Service</h1>
            <p className="text-sm text-muted-foreground">Last updated: {new Date().toLocaleDateString()}</p>
            
            <div className="space-y-6 text-foreground/90 leading-relaxed">
                <section>
                    <h2 className="text-2xl font-semibold mb-3">1. Acceptance of Terms</h2>
                    <p>
                        By accessing and using RedAlert ("the Service"), you accept and agree to be bound by the terms and provision of this agreement. 
                        In addition, when using this Service, you shall be subject to any posted guidelines or rules applicable to such services.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">2. Description of Service</h2>
                    <p>
                        RedAlert is a unified product safety and recall intelligence platform. We aggregate, standardize, and score product safety alerts from various government bodies and public news sources to provide a centralized dashboard for consumers.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">3. Disclaimer of Warranties and Accuracy of Information</h2>
                    <p className="mb-2">
                        <strong>The Service is provided on an "AS IS" and "AS AVAILABLE" basis.</strong>
                    </p>
                    <p className="mb-2">
                        While we strive to provide accurate and up-to-date information, RedAlert does not guarantee the accuracy, completeness, timeliness, or correct sequencing of the recall and safety information aggregated. The information presented on this platform is gathered from third-party public sources and automated NLP (Natural Language Processing) systems, which may occasionally produce errors or miscategorizations.
                    </p>
                    <p>
                        RedAlert is not an official government entity or manufacturer representative. You should always verify safety warnings and recall instructions directly with the product's manufacturer or the relevant government regulatory agency (such as the FDA, CPSC, NHTSA in the US, or FSSAI and CDSCO in India) before taking any action.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">4. Limitation of Liability</h2>
                    <p>
                        In no event shall RedAlert, its developers, or its affiliates be liable for any direct, indirect, incidental, special, consequential or exemplary damages, including but not limited to, damages for loss of profits, goodwill, use, data or other intangible losses (even if RedAlert has been advised of the possibility of such damages), resulting from the use or the inability to use the Service or reliance on any information provided on the Service.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">5. User Conduct</h2>
                    <p>
                        You agree not to reproduce, duplicate, copy, sell, resell or exploit any portion of the Service, use of the Service, or access to the Service without the express written permission by RedAlert. Automated scraping of our database without permission is strictly prohibited.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">6. Contact Information</h2>
                    <p>
                        If you have any questions regarding these Terms of Service, please contact us at: <a href="mailto:bipulnandan276@gmail.com" className="text-primary hover:underline">bipulnandan276@gmail.com</a>
                    </p>
                </section>
            </div>
        </div>
    );
}
