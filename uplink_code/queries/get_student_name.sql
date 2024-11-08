SELECT TOP 1
    P.PERSON_CODE AS Personcode,
    P.FORENAME + ' ' + P.SURNAME AS Firstname
FROM ebslive.dbo.PEOPLE_UNITS AS PU
LEFT JOIN ebslive.dbo.PEOPLE AS P ON P.person_code = PU.person_code
WHERE PU.Person_Code = ?
AND PU.UNIT_TYPE = 'R'