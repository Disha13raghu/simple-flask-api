from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app= Flask(__file__)


app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///db"
db= SQLAlchemy(app)
api= Api(app)
app.app_context().push()


#models
class Employees(db.Model):
    ids= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String, nullable= False)
    salary=db.Column(db.Float,nullable=True)
    
class Employeesapi(Resource):
    def get(self):# read the data
        emp_data= Employees.query.all()
        emp_list=[]
        for e in emp_data:
            emp_list.append({"id":e.ids, "name":e.name, "salary":e.salary})
        return emp_list    
        
        
    def post(self):#create the record
        new_emp= Employees(name=request.json["name"], salary=request.json["salary"])
        db.session.add(new_emp)
        db.session.commit()
        return{"message":"added successfully"},200
    
    def put(self,id):# update record
        data= Employees.query.filter_by(ids=id).first()
        if data:
            data.name=request.json["name"]
            data.salary=request.json["salary"]
            db.session.commit()
            return {"message":"updated successfully"},200
        return {"message":"id not found"},404
            
    
    def delete(self,id): # delete record           
        data=   Employees.query.filter_by(id).first()
        if data:
            db.session.delete(data)
            db.session.commit()
            return {"message":"deleted successfully"},200
        return {"message":"id not found"},404
    
class Employeessearchapi(Resource):
    def get(self,id):# read the data
        emp_data= Employees.query.filter_by(ids=id).first()
        if emp_data:
            emp_list=[{"id":id, "name":emp_data.name, "salary":emp_data.salary}]
            return emp_list
        return {"message":"id not found"}, 404 

    
api.add_resource(Employeesapi, "/employees","/employees/update/<int:id>","/employees/delete/<int:id>")
api.add_resource(Employeessearchapi,"/employees/<int:id>")


        

app.run(debug=True)