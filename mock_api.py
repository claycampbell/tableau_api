from flask import Flask, jsonify
from flask_graphql import GraphQLView
import graphene
from graphene import ObjectType, String, List, Field
from collections.abc import Mapping
from collections.abc import MutableMapping
from collections.abc import Sequence

app = Flask(__name__)

# GraphQL Schema Definitions
class Calculation(ObjectType):
    name = String()
    dataType = String()
    formula = String()
    role = String()

class FieldData(ObjectType):
    name = String()
    referencedByCalculations = List(Calculation)

class EmbeddedDatasource(ObjectType):
    name = String()
    fields = List(FieldData)

class Workbook(ObjectType):
    name = String()
    embeddedDatasources = List(EmbeddedDatasource)

class Query(ObjectType):
    workbooks = List(Workbook)

    def resolve_workbooks(self, info):
        # Return your mock data here
        return mock_data_extract_referenced_calculations['data']['workbooks']

schema = graphene.Schema(query=Query)

# Flask Routes
@app.route('/downstream_harm', methods=['POST'])
def downstream_harm():
    mock_data = {
        "datasources": [
            {
                "id": "05d90d0e-102d-b4e0-e7d0-164fca98b657",
                "name": "Snowflake Connection Region",
                "downstreamSheets": [
                    {"id": "00fbdeb9-feda-aa01-0c37-96a9701f8137", "name": "Projected Total Price"}
                ],
                "downstreamWorkbooks": [
                    {"id": "1e327a28-978f-e8f5-b99c-accf38be67dd", "name": "Customers by Segment"}
                ]
            }
            # ... add other datasources if needed
        ]
    }
    return jsonify(mock_data)

@app.route('/extract_referenced_calculations', methods=['POST'])
def extract_referenced_calculations():
    return jsonify(mock_data_extract_referenced_calculations)

# Mock Data
mock_data_extract_referenced_calculations = {
    "data": {
        "workbooks": [
            {
                "name": "Product Sub List",
                "embeddedDatasources": [
                    {
                        "name": "MARKET_PROD_SUBS_SD (ANALYTICS.MARKET_PROD_SUBS_SD) (ANALYTICS)",
                        "fields": [
                            {
                                "name": "Market",
                                "referencedByCalculations": []
                            },
                            # ... (rest of the provided data)
                        ]
                    }
                ]
            }
        ]
    }
}

# Adding GraphQL endpoint
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Set to False if you don't want the in-browser IDE
    )
)

if __name__ == '__main__':
    app.run(debug=True)
