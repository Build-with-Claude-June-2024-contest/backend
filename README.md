# Backend

## About

Finding suitable talent is challenging. It requires using various platforms with different queries, and these queries need to be optimized. This process takes experience and trial and error.

We use Claude API to transform natural language requirements into optimized search queries according to best practices, and show the data to the user. This makes it easier to find the talent users need.

## Table of Contents

- [Backend](#backend)
  - [About](#about)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
    - [Features](#features)
    - [Installation](#installation)
    - [Migration](#migration)
    - [Contributing](#contributing)
    - [License](#license)
    - [Acknowledgments](#acknowledgments)

## Getting Started

### Features

- Transform natural language requirements into optimized search queries.
- Utilize Claude API for query optimization.
- Simplify the talent search process.

### Installation

1. **Install dependencies:**

    ```bash
    poetry install
    ```

2. **Create a `.env` file and input environment variables:**

    ```bash
    cp env.example .env
    ```

3. **Initialize database tables:**

    ```bash
    alembic upgrade head
    ```

4. **Start the application in development mode:**

    ```bash
    uvicorn app.main:app --reload
    ```

### Migration

1. **Make migrations:**

    ```bash
    alembic revision --autogenerate -m "migration message"
    ```

2. **Apply migrations:**

    ```bash
    alembic upgrade head
    ```

### Contributing

We welcome contributions from the community. To contribute:

1. Fork this repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes.
4. Commit your changes: `git add . && git commit -m "Add some feature"`.
5. Push to the branch: `git push origin feature-branch`.
6. Open a pull request.

Please read our [Contributing Guide](link-to-contributing-guide) for more details.

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

- Thanks to the developers of the [Anthropic Claude API](https://www.anthropic.com/api) for their amazing work.
- Inspired by the best practices from [Better README](https://github.com/schultyy/better-readme) and [Readmine](https://github.com/mhucka/readmine).
