PUBMED_PROMPT = """Extract below entities from the document in JSON format. This document is a part of Journal. Tf no values are present, specilfy "Null".
            {
                "Volume": <volume number of the document>,
                "Number": <number of the volume>,
                "DatePublished": <Date on which the Journal is published>,
                "Title": <Title of the document>,
                "Journal": <Full name of the Journal>,
                "Pages" : <start-end page numbers of this document from the Journal>,
                "DOI": <all characters of the url, after http://dx.doi.org/ or http://doi.org/ or https://doi.org/>,
                "Abstract": <Generate the Abstract>,
                "FirstAuthor": <pick the 1st Author from the list of authors>,
                "Authors" : <mention all the authors of the Journal and exclude the acadamic degrees in the suffix of the name and also exclude the First Author from the list>,
                "ClinicalTrailNumbers": <Clinical Trail Number>,
                "Product" : <name of the Product>,
                "Indications": <Therapeutic indication(s)>,
                "Keywords": <Keywords>
            }
            important instructions to follow while generating values:
            1. remove new line characters
            2. Abstract should be very conscise.
            3. Refer to https://pubmed.ncbi.nlm.nih.gov to obtain full Journal name
            4. Seperate the Keywords with semicolumn(;)
            5. Do not use abbrivations for Indication.
            6. Seperate the Authors with semicolumn(;)
            7. Do not change the format for "Authors" value.
            8. only "First Author" should be in the format: "Last name, First name"
"""