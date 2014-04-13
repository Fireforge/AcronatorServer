AcronatorServer
===============

Back-end code to Fireforge/Acronator

The Website: www.github.com/Fireforge/Acronator


### API: ###
  `http://api.acronator.com/<youracronym>&<your keywords sperated by spaces>`
  
  This returns JSON with:
    
    {
      "result": ["acronym1", "acronym2", "acronym3", ...],
      "acronym": "youracronym",
      "des": "your keywords sperated by spaces"
    }
    
### Example: ###
  GET: http://api.acronator.com/hello&world%20foo%20bar
  
  Result:
  
    {
      "result": ["hours eyes looks looks officials", "having email leaders leaders opportunity", "health election leader leader ones"],
      "acronym": "hello",
      "des": "world"
    }
    

