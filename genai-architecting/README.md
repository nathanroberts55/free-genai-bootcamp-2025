# Architecting GenAI

![Sentence Generator Architectual Diagram](genai-architecture.png)

## Requirements

### Overview

Based in Kansas City, MO, our company is dedicated to providing high-quality, culturally relevant language education through an innovative and user-friendly application. Our primary goal is to support a globally dispersed student base, currently numbering 1,500 and growing by 150 students annually, by offering personalized learning experiences that cater to diverse backgrounds and proficiency levels. We aim to leverage cutting-edge AI and machine learning technologies to create adaptive learning paths and interactive tools, ensuring an engaging and effective learning journey. As we expand our library of languages and enhance our platform, we are committed to maintaining scalability, security, and user satisfaction, positioning ourselves as a leader in the language education market with significant growth potential.

### Architectural/Design Considerations

#### Requirements, Risks, Assumptions, & Constraints

**Requirements:**

- **Business Requirements:**
  - Expand language offerings beyond Japanese.
  - Enhance student engagement and learning outcomes.
  - Integrate AI-driven tools to augment instructor-led classes.

- **Functional Requirements:**
  - Develop various AI-powered learning apps (e.g., visual novel generator, text adventure, sentence constructor).
  - Support multiple languages and provide real-time feedback.
  - Integrate with the existing learning portal and learning record store.

- **Non-functional Requirements:**
  - Ensure high performance and scalability to handle concurrent users.
  - Maintain robust security and privacy measures.
  - Provide a user-friendly and accessible interface.

- **Tooling:**
  - Evaluate the use of Generative AI (GenAI) vs. traditional Machine Learning (ML) based on specific use cases.

**Risks:**

- **Technical Risks**:  Potential issues with the availability of AI/ML platforms and models, risks associated with hosting services (self-hosting vs. cloud hosting), and challenges in managing data security and ensuring redundancy of user data.
- **Project Risks**: Delays in development, budget overruns, and changes in business/stakeholder requirements.
- **Operational Risks**: User adoption challenges, maintenance issues, and support requirements.

**Assumptions:**

- The existing learning portal and record store are compatible with new AI tools.
- Students have access to necessary hardware (e.g., webcams for ASL practice).
- The school has a budget for cloud/on-prem infrastructure and AI development.

**Constraints:**

- **Budget**: Fixed budget for development and maintenance.
- **Timeline**: Specific deadlines for project milestones and final delivery.
- **Regulatory Compliance**: Adherence to educational, local/regional, or national data protection regulations (e.g., GDPR, CCPA).
- **Technical Limitations**: Constraints related to existing infrastructure and technology stack.

### Data Strategy

**Data Collection and Preparation:**

- Collect diverse datasets for language learning, including text, audio, and video.
- Ensure data is labeled and preprocessed for training AI models.

**Data Quality and Diversity:**

- Use high-quality, diverse datasets to improve model accuracy and generalization: Ensure datasets include a wide range of language contexts, such as conversational dialogues, formal texts, and slang, to cover various learning scenarios. For example, collecting dialogues from Japanese TV shows, news articles, and social media posts can provide a rich and varied dataset.

- Regularly update datasets to reflect current language usage and trends: Continuously incorporate new data sources to keep the language models up-to-date with evolving language patterns. For instance, periodically scraping recent blog posts, tweets, and online forums can help capture the latest vocabulary and usage trends.

**Privacy and Security Concerns:**

- Implement strong encryption and access controls to protect student data.
- Ensure compliance with data privacy regulations (e.g., GDPR, FERPA).
- Host models locally or on a private instance to ensure user input data remains secure and under control. This approach minimizes the risk of data breaches and provides greater oversight over data handling practices.

**Integration with Existing Data Systems:**

- Develop APIs to integrate new AI tools with the existing learning portal and record store.

### Model Selection and Development

**Model Considerations:**

Certainly! Here are the expanded points with details relevant to business partners:

**Model Considerations:**

- **Self-Hosted vs. SaaS:** Evaluate the cost and performance trade-offs, considering factors such as data privacy, control over updates, and potential long-term savings with self-hosted solutions versus the ease of maintenance and scalability offered by SaaS providers.
- **Open Weight vs. Open Source:** Consider licensing and customization needs, ensuring that the chosen models align with the business's budget and flexibility requirements, and assess the potential for community support and contributions with open-source options.
- **Input-Output:** Determine the best models for text-to-text, speech-to-text, etc., based on the specific learning app requirements, ensuring they can handle the expected input and output formats efficiently.
- **Number of Models Needed:** Assess based on different learning apps, ensuring that each app has a dedicated model or shared models where appropriate to optimize resource usage and performance.
- **Number of Calls/Model:** Estimate usage to plan for scalability, considering peak times and the number of concurrent users to ensure the infrastructure can handle the load without performance degradation.
- **Size and Evaluation:** Choose models that balance performance and efficiency, taking into account the computational resources required and the expected response times to provide a smooth user experience.
- **Context Window:** Optimize input and output lengths for each use case, ensuring that the models can handle the necessary context without excessive computational overhead.
- **Fine-Tuning Requirements:** Plan for domain-specific fine-tuning to improve model accuracy and relevance, considering the availability of labeled data and the expertise required for fine-tuning.
- **Model Performance and Efficiency:** Regularly benchmark and optimize models to ensure they meet performance standards and provide the best possible user experience, while also keeping operational costs in check.

### Infrastructure Design

**Scalable and Flexible Infrastructure:**

- Leverage cloud platforms (e.g., AWS, Azure, GCP) for scalability and specialized hardware.
- Implement a modular architecture for easy updates and component replacements.
- Consider hybrid or multi-cloud approaches for cost-efficiency and performance.

### Integration and Deployment

**Seamless Integration:**

- Develop APIs and interfaces for easy access to AI capabilities.
- Implement CI/CD pipelines for continuous integration and deployment.
- Ensure compatibility with legacy systems to avoid disruptions.

### Monitoring and Optimization

**Robust Monitoring:**

- Implement logging and telemetry to monitor model performance.
- Set up feedback loops for continuous improvement.
- Develop KPIs to measure the business impact of AI solutions.
- Set up billing alerts to monitor usage and control costs.

### Governance and Security

**Strong Governance and Security:**

- Develop policies for responsible AI use.
- Implement access controls and data protection measures.
- Ensure compliance with relevant regulations and industry standards.

### Scalability and Future-Proofing

**Scalable and Future-Proof Architecture:**

- Use containerization and microservices for flexibility.
- Implement version control for models and data.
- Plan for potential increases in computational requirements.
