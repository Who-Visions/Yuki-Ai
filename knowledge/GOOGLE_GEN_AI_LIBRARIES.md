# Google Gen AI libraries

This page provides information on downloading and installing the latest libraries for the Gemini API. If you're new to the Gemini API, get started with the API quickstart.

> **Important note about google-genai libraries**
> We've recently launched a new set of libraries that provide a more consistent and streamlined experience for accessing Google's generative AI models across different Google services.
>
> Vertex AI libraries are only supported on the Vertex AI platform.

## Key library updates

| Language | Vertex AI library | New library (Recommended) |
| :--- | :--- | :--- |
| **Python** | `google-cloud-aiplatform`<br>GenerativeModel Module Deprecated in May 2026 | `google-genai` |
| **Go** | `cloud.google.com/vertexai`<br>Deprecated in May 2026 | `google.golang.org/genai` |
| **JavaScript and TypeScript** | `@google-cloud/vertexai`<br>Deprecated in May 2026 | `@google/genai`<br>Available in Preview |
| **Java** | `google-cloud-vertexai`<br>Deprecated in May 2026 | `java-genai`<br>Available in Preview |

Users are encouraged to start with the new library and migrate from previous libraries.

## Install a library
The following examples can help you get started in various programming languages.

### Python
You can install our Python library by running:

```bash
pip install google-genai
```

### Go
You can install our Go library by running:

```bash
go get google.golang.org/genai
```

### JavaScript and TypeScript
You can install our JavaScript and TypeScript library by running:

```bash
npm install @google/genai
```

The new JavaScript and TypeScript library is available in preview, which means it may not be feature complete and that we may need to introduce breaking changes.

However, we highly recommend you start using the new SDK over the previous, deprecated version as long as you're comfortable with these caveats. We're actively working towards a GA (General Availability) release for this library.

### Java
You can install our Java library by adding the dependencies in Maven:

```xml
<dependencies>
  <dependency>
    <groupId>com.google.genai</groupId>
    <artifactId>google-genai</artifactId>
    <version>0.8.0</version>
  </dependency>
</dependencies>
```

The new Java library is available in preview, which means it may not be feature complete and that we may need to introduce breaking changes.

However, we highly recommend you start using the new SDK over the previous, deprecated version as long as you're comfortable with these caveats. We're actively working towards a GA (General Availability) release for this library.
