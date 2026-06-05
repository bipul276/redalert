export default function Compliance() {
    return (
        <div className="max-w-3xl mx-auto space-y-8 py-8 px-4">
            <h1 className="text-3xl font-bold tracking-tight text-foreground sm:text-4xl">Compliance & Data Sources</h1>
            <p className="text-sm text-muted-foreground">Information on how we collect, process, and display public safety data.</p>
            
            <div className="space-y-6 text-foreground/90 leading-relaxed">
                <section>
                    <h2 className="text-2xl font-semibold mb-3">1. Our Role as an Aggregator</h2>
                    <p>
                        RedAlert operates strictly as an information aggregator. We do not issue product recalls, nor do we perform independent product testing or investigations. 
                        Our platform automatically collects, standardizes, and scores safety alerts that have already been made public by recognized authorities and news outlets.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">2. Primary Data Sources</h2>
                    <p className="mb-2">RedAlert integrates data from several official and public sources, categorizing them by region:</p>
                    
                    <h3 className="text-xl font-medium mt-4 mb-2 text-foreground">United States</h3>
                    <ul className="list-disc pl-6 space-y-1 mb-4">
                        <li><strong>CPSC:</strong> Consumer Product Safety Commission.</li>
                        <li><strong>FDA:</strong> Food and Drug Administration.</li>
                        <li><strong>NHTSA:</strong> National Highway Traffic Safety Administration.</li>
                    </ul>

                    <h3 className="text-xl font-medium mt-4 mb-2 text-foreground">India</h3>
                    <ul className="list-disc pl-6 space-y-1 mb-4">
                        <li><strong>FSSAI:</strong> Food Safety and Standards Authority of India.</li>
                        <li><strong>CDSCO:</strong> Central Drugs Standard Control Organisation.</li>
                        <li><strong>Google News RSS:</strong> Verified public news outlets reporting on product bans, seizures, or safety investigations.</li>
                    </ul>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">3. Data Processing and NLP Engine</h2>
                    <p className="mb-2">
                        Because safety alerts are often scattered and unstructured (particularly in news reports), RedAlert employs a Natural Language Processing (NLP) engine to structure this data:
                    </p>
                    <ul className="list-disc pl-6 space-y-2">
                        <li><strong>Deduplication:</strong> Identifying and merging duplicate reports of the same recall incident from different sources.</li>
                        <li><strong>Region Scoring:</strong> Determining the primary affected region (e.g., distinguishing between a product manufactured in one country but recalled in another).</li>
                        <li><strong>Confidence Levels:</strong> We assign confidence scores ("Confirmed", "Probable", "Watch") based on the authority of the source. Official government sources receive the highest confidence ratings.</li>
                    </ul>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">4. Fair Use and Copyright</h2>
                    <p>
                        The summaries, titles, and public alerts displayed on RedAlert are distributed under the doctrine of Fair Use for the purpose of public safety and news reporting. 
                        We provide attribution and link back to original sources where applicable. We do not claim copyright over official government recall statements.
                    </p>
                </section>

                <section>
                    <h2 className="text-2xl font-semibold mb-3">5. Report Inaccuracies</h2>
                    <p>
                        If you are a manufacturer or official representative and believe a safety alert is displayed inaccurately or lacks recent updates, please reach out to us immediately for correction at: <a href="mailto:bipulnandan276@gmail.com" className="text-primary hover:underline">bipulnandan276@gmail.com</a>
                    </p>
                </section>
            </div>
        </div>
    );
}
