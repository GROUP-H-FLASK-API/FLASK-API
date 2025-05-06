from flask import Blueprint, request, jsonify
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_404_NOT_FOUND,HTTP_200_OK,HTTP_403_FORBIDDEN
import validators
from app.models.company_model import Company
from app.models import author_model
from app.models.author_model import Author
from app.extensions import db,bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, create_refresh_token

#company blueprint
companies = Blueprint('companies', __name__,
                        url_prefix='/api/v1/companies') #creating a new object


#creating companies
@companies.route("/create", methods = ['POST'])
@jwt_required()
def create_company():

    #storing request values
    data = request.json
    name = data.get("name")
    location = data.get("location")
    contact = data.get("contact")
    email = data.get("email")
    company_id = data.get("company_id")
    author_id = get_jwt_identity()


    #validations of the company requests
    if not name or not location or not email:
        return jsonify({"Error":"All fields are required"}),HTTP_400_BAD_REQUEST

    if Company.query.filter_by(name=name).first() is not None:
        return jsonify({"Error":"Company name is already in use"}),HTTP_409_CONFLICT
    
    try:

        #creating a new company
        new_company = Company(name=name,contact=contact,location=location,email=email,author_id=author_id,company_id=company_id)
        db.session.add(new_company)
        db.session.commit()


        return jsonify({"Message":name + "has been successfully created ",
                        "company":{
                            "id":new_company.company_id,
                            "name":new_company.name,
                            "location":new_company.location,
                            "email":new_company.email,
                            "contact":new_company.contact,
                            "author_id":new_company.author_id,
                                  }
                        }),HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"Error":str(e)}),HTTP_500_INTERNAL_SERVER_ERROR
    
#getting all companies
@companies.get('/')
@jwt_required()
def getallcompanies():



    # email = request.json.get("email")
    # password = request.json.get("password")

    try:

        all_companies = Company.query.all()


        companies_data = []

        for company in all_companies:
            company_info = {
                "id" : company.company_id,
                "name" : company.name,
                "contact" : company.contact,
                "email" : company.email,
                "location" : company.location,
                "author" : {
                        "first_name":company.author.fname,
                        "last_name":company.author.lname,
                        "contact":company.author.contact,
                        "email":company.author.email,
                        "created_at" : company.author.created_at
                },
                "created_at" : company.created_at
                }
            
            companies_data.append(company_info)

        return jsonify({
            "Message": "All companies retrieved successfully",
            "total companies": len(companies_data),
            "companies":companies_data
        }),HTTP_200_OK #serializing the data enables us have a variable that can be converted to jsony easily
        
    except Exception as e:
        return  jsonify({
            "Error":str(e)
        }), HTTP_500_INTERNAL_SERVER_ERROR
    



#getting a company by id
@companies.get('/company/<int:company_id>')
@jwt_required()
def getcompany(company_id):
        
        

        try:
            company = Company.query.filter_by(company_id = company_id).first()

            if not company:
                 return jsonify({
                      "Error":"company not found"
                 }),HTTP_404_NOT_FOUND
            return jsonify({
                 "Message": "Company retrieved successfully",
                 "companies":{
                      "id":company.company_id,
                      "name":company.name,
                      "location":company.location,
                      "contact":company.contact,
                      "email":company.email,
                      "author": {
                            "first_name":company.author.fname,
                            "last_name":company.author.lname,
                            "contact":company.author.contact,
                            "email":company.author.email,
                            "biography":company.author.biography,
                            "created_at":company.author.created_at
                      },
                      "created_at":company.created_at
                    #   "books": books
                      }
                 }),HTTP_200_OK
        except Exception as e:
            return  jsonify({
                 "Error":str(e)
                 }), HTTP_500_INTERNAL_SERVER_ERROR
    

# updating company details
@companies.route('/edit/<int:company_id>', methods = ['PUT','PATCH']) #working with the route function
@jwt_required() # protects the route
def UpdateCompanyDetails(company_id):
        
        

        try:

            current_author = int(get_jwt_identity()) #returns the identity of a currently logged in author
            loggedinauthor = Author.query.filter_by(author_id = current_author).first()

            # get company by id
            company = Company.query.filter_by(company_id=company_id).first()

            if not company:
                 return jsonify({
                      "Error":"Company not found"
                 }),HTTP_404_NOT_FOUND
            elif company.author_id!=current_author:
                 return jsonify({
                      "Error":"You are not authorized to update the company details"
                 }),HTTP_403_FORBIDDEN
            else:
                 name = request.get_json().get("name", company.name)
                 email = request.get_json().get("email", company.email)
                 contact = request.get_json().get("contact", company.contact)
                 location = request.get_json().get("location", company.location)

                 

                 if contact != company.contact and Company.query.filter_by(contact = contact).first():
                      return jsonify({
                           "Error": "contact already in use"
                      }),HTTP_409_CONFLICT

                 company.name = name
                 company.location = location
                 company.contact = contact
                 company.email = email

                 db.session.commit()



                 return jsonify({
                      'message': name + "'s details have been updated successfully",
                      'company' : {
                           "id":company.company_id,
                            "name":company.name,
                            "location":company.location,
                            "contact":company.contact,
                            "email":company.email,
                            "created_at":company.created_at
                      },
                      "created_at":company.created_at
                 })

                      


        except Exception as e:
            return  jsonify({
                 "Error":str(e)
                 }), HTTP_500_INTERNAL_SERVER_ERROR


# deleting a company
@companies.route('/delete/<int:company_id>', methods = ['DELETE']) #working with the route function
@jwt_required() # protects the route
def deletecompany(company_id):
        
        

        try:

            current_author = int(get_jwt_identity()) #returns the identity of a currently logged in author
            loggedinauthor = Author.query.filter_by(author_id = current_author).first()
             
          # getting a company by id
            company = Company.query.filter_by(company_id=company_id).first()

            if not company:
                 return jsonify({
                      "Error":"Company not found"
                 }),HTTP_404_NOT_FOUND
            elif company.author_id!=current_author:
                 return jsonify({
                      "Error":"You are not authorized to update the author details"
                 }),HTTP_403_FORBIDDEN
            else:

                  #delete associated books
                 for book in company.books:
                      db.session.delete(book)

                 db.session.delete(company)
                 db.session.commit()

                 return jsonify({
                      'message': "Company deleted successfully",
                 })

        except Exception as e:
            return  jsonify({
                 "Error":str(e)
                 }), HTTP_500_INTERNAL_SERVER_ERROR    



# # searching an author
# @authors.get('/search')
# @jwt_required()
# def searchAuthors():

#     try:

#         search_query = request.args.get('query','')

#         authors = Author.query.filter( or_ (Author.fname.ilike(f"%{search_query}%"),
#                                        Author.lname.ilike(f"%{search_query}%"))).all()
        
#         if len(authors) == 0:
#              return jsonify({
#                   'message':'No results found'
#              }),HTTP_404_NOT_FOUND
#         else:
             
#              authors_data = []

#         for author in authors:
#             author_info = {
#                 "id" : author.author_id,
#                 "first_name" : author.fname,
#                 "last_name" : author.lname,
#                 "author_name" : author.get_full_name(),
#                 "email" : author.email,
#                 "contact" : author.contact,
#                 "created_at" : author.created_at,
#                #  "companies": [],
#                #  "books": []
#                 }
            
#             authors_data.append(author_info)

#         return jsonify({
#             "Message": f"Authors with name {search_query} retrieved successfully",
#             "total search": len(authors_data),
#             "search_results":authors_data
#         }),HTTP_200_OK #serializing the data enables us have a variable that can be converted to jsony easily
        
#     except Exception as e:
#         return  jsonify({
#             "Error":str(e)
#         }), HTTP_500_INTERNAL_SERVER_ERROR    
