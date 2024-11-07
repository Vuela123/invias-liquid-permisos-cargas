import os
from dotenv import load_dotenv
from pymongo import MongoClient

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class MongoDBClient:
    """
    Clase Singleton para manejar la conexión a MongoDB.

    Asegura que sólo exista una instancia del cliente de MongoDB durante la vida útil de la aplicación,
    proporcionando un único punto de acceso global para la conexión a la base de datos.

    Attributes:
        _instance (MongoDBClient, opcional): Mantiene la instancia única de la clase.
        _client (MongoClient): Cliente de MongoDB utilizado para conectar con la base de datos.
        _database (Database): Instancia de la base de datos MongoDB.
    """

    _instance = None

    def __new__(cls):
        """
        Crea o retorna la única instancia de MongoDBClient.
        
        Returns:
            MongoDBClient: La única instancia de esta clase.
        """
        if cls._instance is None:
            cls._instance = super(MongoDBClient, cls).__new__(cls)
            try:
                mongo_url = os.getenv("MONGO_URL")
                mongo_db = os.getenv("MONGO_DB")
                if not isinstance(mongo_db, str) or not mongo_db:
                    raise ValueError("MONGO_DB debe ser una cadena no vacía")

                cls._client = MongoClient(mongo_url)
                cls._client.admin.command('ping')
                print("Conexión a MongoDB establecida y verificada con éxito.")
                cls._database = cls._client[mongo_db]
            except Exception as e:
                print(f"Error al conectar con MongoDB: {e}")
                raise
        return cls._instance

    @classmethod
    def get_database(cls):
        """
        Retorna la instancia de la base de datos MongoDB asociada con la instancia única del cliente.

        Returns:
            Database: La instancia de la base de datos MongoDB.
        """
        return cls._database