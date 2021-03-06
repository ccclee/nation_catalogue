def nationDict():
    """
    Helper function that returns a dictionary of the nation database
    
    Returns:
        dict: A dictionary of nation data from nation database
    """
    # Create a dict of the nation table in a dictionary format based on ID
    nationdict = {}
    nationrows = db(db.nation).select()
    for x in nationrows:
        nation_data ={}
        nation_data["nation_name"] = x.nation_name
        nation_data["nation_description"] = x.nation_description
        nation_data["nation_size"] = x.nation_size
        nation_data["nation_flag"] = x.nation_flag
        nation_data["nation_wikipedia_link"] = x.nation_wikipedia_link
        nation_data["nation_type"] = x.nation_type
        nation_data["nation_birth_year"] = x.nation_birth_year
        nation_data["nation_end_year"] = x.nation_end_year
        nation_data["nation_year_type_birth_year"] = x.nation_year_type_birth_year
        nation_data["nation_year_type_end_year"] = x.nation_year_type_end_year
        nation_data["nation_date_added"] = x.nation_date_added
        nation_data["is_deleted"] = x.is_deleted
        nationdict[x.id] = nation_data
    return nationdict

def helperFilterNation(query, nationdict):
     """
     Helper function that returns the resulting string from a given query and database dictionary
     
     Args:
        query::Obj
            A SQL query given from filterNation()
        nationdict::dict
            A dictionary of the nation database
        
        
     Returns:
        str: The resulting string of the HTML produced from the query
     """
     # If not empty query, then return the HTML of what is needed
     if len(query) != 0:
       return_message = ""
       i = 0
       while i < len(query):
         query_elements = query[i]
         nation_id = query_elements[0]
         # Tests to verify if the element is correct
         #return_message = format(nationdict[nation_id]["nation_name"])

         # Create the the HTML based on selected dictionary
         return_html = ""
         # Format for size of a nation
         format_of_size = '{:,}'.format(nationdict[nation_id]["nation_size"])
         return_html = return_html + "<div class='row catalogueRow'><img class='col col-lg-4 col-md-4 col-sm-4 nation_flag' src='/nation_catalogue/static/flags/" + nationdict[nation_id]["nation_flag"] +"' alt='nation flag'/>"
                    
         return_html = return_html + "<div class='col col=lg-8'><h1><b><a href='" + nationdict[nation_id]["nation_wikipedia_link"] +"' target='_new'>" + nationdict[nation_id]["nation_name"] +"</a></b></h1><hr><div class='descriptionDiv'><p><b>Description: </b>" + nationdict[nation_id]["nation_description"] +"</p>"
                    
         return_html = return_html +  "<p><b>Size: </b>" + format_of_size + " km<sup>2</sup></p><p><b>Nation Type: </b>" + nationdict[nation_id]["nation_type"] +"</p><p><b>Lifespan: </b>"
         return_html = return_html + format(nationdict[nation_id]["nation_birth_year"]) + format(nationdict[nation_id]["nation_year_type_birth_year"]) +" - " + format(nationdict[nation_id]["nation_end_year"]) + format(nationdict[nation_id]["nation_year_type_end_year"])+"</p>"
                    
         return_html = return_html + "<p><button class='customButton updateNation' data-attr='"+ format(nation_id) + "'>Update Nation Data</button><button class='customButton deleteNation' data-attr='"+ format(nation_id) + "'>Delete Nation Data</button></p></div></div></div>"
                    
         return_message = return_message + return_html
                            
         i = i + 1
     # Else return empty query to display a filter message
     else:
       return_message = "empty query"

     return return_message

def filterNation():
    """
    Filters a nation data based on the data that is passed in
    
    """
    if request.ajax:
        # Get the variables if request is ajax
        nationType = request.vars.nationType
        year = request.vars.year
        yearType = request.vars.yearType
        
        # Get the nation dict
        nationdict = nationDict()
        query = ""
        select_query = ""
        # If nationType is ALL
        if nationType=="All":
            # Case 1: If year is AD 
            if (yearType == "AD"):
                select_query = "SELECT * FROM nation WHERE (? BETWEEN nation_birth_year AND nation_end_year) AND is_deleted=0"
            # Case 2: If year is BC:
            elif (yearType == "BC"):
               # Complex: Would be to compare year with birth_year and 1 BC. Year 0 does not exist so no need to worry about 0.
               select_query = "SELECT * FROM nation WHERE (? BETWEEN nation_birth_year AND 1) AND is_deleted=0"
            query = db.executesql(select_query, placeholders=(year,))
            return_message = helperFilterNation(query, nationdict)
        else:
            # Case 1: If year is AD 
            if (yearType == "AD"):
                select_query = "SELECT * FROM nation WHERE (? BETWEEN nation_birth_year AND nation_end_year) AND nation_type=? AND is_deleted=0"
            # Case 2: If year is BC:
            elif (yearType == "BC"):
               # Complex: Would be to compare year with birth_year and 1 BC. Year 0 does not exist so no need to worry about 0.
               select_query = "SELECT * FROM nation WHERE (? BETWEEN nation_birth_year AND 1) AND nation_type=? AND is_deleted=0"
            query = db.executesql(select_query, placeholders=(year, nationType))
            return_message = helperFilterNation(query, nationdict)

        return return_message
    
def deleteNation():
    """
    Deletes an existing nation data from the database based on the ID passed in.
    
    """
    # Delete the nation data if the request was done via AJAX
    if request.ajax:
        # ID # is passed in the url from request.args(0). Depending on what is in the url, show ID data. Else if ID doesn't exist, redirect. 
        nation_id = request.vars.value
        update_query = db(db.nation.id == nation_id).update(is_deleted='1')


def update_nation():
    """
    Update an existing nation data from the database where a record is generated based on the ID passed in.
    
    Returns:
        Obj: A SQLFORM
    """
    # ID # is passed in the url from request.args(0). Depending on what is in the url, show ID data. Else if ID doesn't exist, redirect to add nation page
    nation_id = request.args(0);
    nation_record = db.nation(nation_id) or redirect(URL('add_nation'))
    # get row from the database if it's not deleted
    if nation_record.is_deleted==0:
        form = SQLFORM(db.nation, nation_record)
        # If record is accepted, redirect back to the nation catalogue
        if form.process().accepted:
            response.flash = T('The nation data has been updated.')
            redirect(URL('view'))
        else:
            response.flash = T('Please complete the form to complete the nation edits.')
    # else if it is, redirect to add_nation page
    else:
        redirect(URL('add_nation'))
    return locals()


def add_nation():
    """
    Creating a powerful form to connect the database we created based on our VALIDATORS automatically.
    Changes some classnames inside the powerful form to a custom class name.
    
    Returns:
        Obj: A SQLFORM
    """
    form = SQLFORM(db.nation)
    form.custom.widget.nation_flag['_class'] = 'custom_nation_flag_box'
    # Set the delete to 0 automatically
    form.vars.is_deleted='0'
    # Customizes submit button widget to a custom class name
    form.element(_type='submit')['_class']='customSubmitButton'
    # If insertion into database is successful, show form accepted and redirect to thank you page
    if form.process().accepted:
        session.flash='The form was successfully submitted.'
        redirect(URL("thanks"))
    # if errors, it will alert
    elif form.errors:
        response.flash = "Submit fail, the form has errors."
    # if first time visit, page, it will give instructions
    else:
        response.flash = "Please fill out the form."
    return locals()

def thanks():
    """
    A return thank you page after successfully submitting a form.
    
    Returns:
        String: A thank you message
    """
    msg = "Thank you for adding a new nation."
    return locals()

def view():
    """
    Displays all the nation data in natio ntable that is not deleted. Order by size of the nation. 
    Allows to extract data from the database and display it on a view page.
    
    Returns:
        Obj: rows from a SQLFORM containing nation data based on size
    """
    rows = db(db.nation.is_deleted==0).select(orderby=~db.nation.nation_size)
    return locals()
