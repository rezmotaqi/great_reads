# from fastapi import Depends, FastAPI
#
# app = FastAPI()
#
#
# # Sample dependencies
# def dependency_a() -> str:
#     return "Dependency A"
#
#
# def dependency_b(a: str = Depends(dependency_a)) -> str:
#     return f"Dependency B received {a}"
#
#
# def dependency_c(a: str = Depends(dependency_b)) -> str:
#     return f"Dependency C received {a}"
#
#
# # Define a service class with a method using dependencies
# class MyService:
#
#     def method_using_dependency(self, b: str = Depends(dependency_c)):
#         print(f"Service Method received: {b}")
#
#
# # Create a function to return the service
# def get_my_service() -> MyService:
#     ss = MyService()
#     ss.method_using_dependency()
#     return ss
#
#
# # Use the service in an endpoint
# @app.get("/")
# async def read_data(service: MyService = Depends(get_my_service)):
#     print(service)
#     return {"result": "result"}


from fastapi import Depends, FastAPI

app = FastAPI()


#
# # Sample dependencies
# def dependency_a() -> str:
#     return "Dependency A"
#
#
# def dependency_b(a: str = Depends(dependency_a)) -> str:
#     return f"Dependency B received {a}"
#
#
# def dependency_c(b: str = Depends(dependency_b)) -> str:
#     return f"Dependency C received {b}"
#
#
# # Define a service class without using Depends directly in methods
# class MyService:
#     def method_using_dependency(self, c_value: str = Depends(dependency_c)):
#         print(f"Service Method received: {c_value}")
#
#
# # Create a function to resolve the dependency and call the method
# def get_my_service(c_value: str = Depends(dependency_c)) -> MyService:
#     service = MyService()
#     # Pass the resolved dependency value to the class method
#     service.method_using_dependency(c_value)
#     return service
#
#
# # Use the service in an endpoint
# @app.get("/")
# async def read_data(service: MyService = Depends(get_my_service)):
#     print(service)
#     return {"result": "Success"}
def func1():
    func3()


def func2():
    func3()


def func4() -> str:
    return "hi"


def func3(testdep: str = Depends(func4)):
    print(testdep)


@app.get("/")
async def read_data():
    func3()
    return {"result": "Success"}
