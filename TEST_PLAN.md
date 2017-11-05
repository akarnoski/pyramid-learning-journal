# Test Plan

**Objective**

Document and track the necessary tests required to thoroughly
verify the application works properly


**Scope**

- list_view
- tag_view
- detail_view
- create_view
- update_view
- verify_delete
- delete_entry

## Testing Strategy

**Unit Tests**

### list_view

- Renders the index.jinja2 file
- GET request needs to return a dictionary of all journal entries in the database

### tag_view

- Renders the tag_list.jinja2 file
- Requested tag must match tag in database
- Each matched entry must be returned by id with all data
- Returns a dictionary of all entries returned by query

### detail_view

- Renders the detail.jinja2 file
- Verifies Entry object in database by id
- Raises exception is id is not valid
- Render to page as dictionary 

### create_view

- Renders the form_page.jinja2 file
- GET request returns and empty dictionary
- POST request takes in user input

### update_view

- Renders the edit_page.jinja2 file
- Verifies Entry object in database by id
- GET request return dict like object of post
- Raises exception is id is not valid
- POST request updates entry

### delete_view

- Renders the delte_view.jinja2 file
- Verifies Entry object in database by id
- GET request return dict like object of post
- Raises exception is id is not valid
- Renders object to the page
- POST request verifies submitted data matches variable
- Delete entry
- Return to page

**Functional Tests**

### list_view

- Each entry must be rendered to the page as an article
- Length of entries must be the same as number of articles
- Entry id should be available in link for opening detail page

### tag_view

- Each matched entry must be returned by id with all data
- Returns a dictionary of all entries returned by query
- Each returned entry must be rendered to the page as an article
- Entry id should be available in link for opening detail page

### detail_view

- Each field in jinja2 file should be filed with entry value

### create_view

- Verifies all fields are filled
- Returns fields that were filled if any are missing
- Save data to render in appropriate form field 
- If the fields are correct but empty values, rerender page
- If all fields are compete, create new instance of Entry object
- Add to database
- Return used to main page

### update_view

- Renders all available data for entry id to correct form fields
- Verifies all fields are filled
- Returns fields that were filled if any are missing
- Save data to render in appropriate form field 
- If the fields are correct but empty values, rerender page
- If all fields are compete, update proper instance of Entry object
- Return used to detail page

