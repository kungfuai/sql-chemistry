<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://www.linkedin.com/company/kungfuai/">
    <img src="https://www.kungfu.ai/wp-content/uploads/2020/06/kungfu-lockup-variant-1.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">KUNGFU.AI SQL Chemistry</h3>

  <p align="center">
    Simplified Database Management on top of SQL Alchemy
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
    * [Built With](#built-with)
* [Getting Started](#getting-started)
    * [Dependencies](#dependencies)
    * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)

### Built With
* [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [Python 3.8](https://www.python.org/)



<!-- GETTING STARTED -->
## Getting Started

This repo aims to simplify the usage of Session, and connection management against Cloud Database Resources.

### Dependencies
Python 3.8

### Installation

`pip install kungfuai-sql-chemistry`

#### Automatic Connection to AWS
Simply create a database dictionary, and call the `register_database` entrypoint.
```python
database_map = {
    "main": AwsDbConfig().detect_db_config("main")
}

register_database(database_map)
```

Notes:
- Place this code in your `__init__.py` in your `src` directory. 
  `AppSession` will know use the engines created from the `register_database` call.
  

- If your environment has a AWS Secret Key, then the auto-detection will use it.
  

- We identify the config based on the input "db_name". For instance, `main` will map to a
  secret key in `env` named MAIN_DB_SECRET_ID.
  

- If no secret ID is found, we search for a db config listing. Please view the example envs to view the requirements.



<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/kungfuai/sql-chemistry/issues) for a list of proposed features (and known issues).


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Endurance Idehen - endurance.idehen@kungfu.ai



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=flat-square
[license-url]: https://github.com/kungfuai/env/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/company/kungfuai/
[product-screenshot]: images/screenshot.png
