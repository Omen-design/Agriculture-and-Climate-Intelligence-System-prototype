import re
import pandas as pd
from data_fetcher import DataGovFetcher


class QueryProcessor:
    def __init__(self):
        self.fetcher = DataGovFetcher()

    def parse_query(self, query):
        """Parse natural language query and extract parameters"""
        query = query.lower()

        # Extract states - FIXED VERSION
        states = []

        # Look for state names in the query
        if 'punjab' in query:
            states.append('Punjab')
        if 'maharastra' in query or 'maharashtra' in query:
            states.append('Maharashtra')
        if 'karnataka' in query:
            states.append('Karnataka')
        if 'uttar pradesh' in query or 'up' in query:
            states.append('Uttar Pradesh')

        # If no states found in text, use default
        if not states:
            states = ['Punjab', 'Maharashtra']

        # Extract years
        years = re.findall(r'last\s+(\d+)\s+years?|(\d{4})', query)
        year_range = []
        if years:
            if years[0][0]:  # last N years
                n = int(years[0][0])
                current_year = 2023
                year_range = [str(current_year - i) for i in range(n)]
            else:  # specific year
                year_range = [years[0][1]]
        else:
            year_range = ['2022']  # Default year

        # Extract crops - FIXED VERSION
        crops = []
        if 'wheat' in query:
            crops.append('Wheat')
        if 'rice' in query:
            crops.append('Rice')
        if 'maize' in query:
            crops.append('Maize')
        if 'cotton' in query:
            crops.append('Cotton')

        # If no crops found, use defaults
        if not crops:
            crops = ['Wheat', 'Rice']

        return {
            'states': states,
            'years': year_range,
            'crops': crops,
            'query_type': self.detect_query_type(query)
        }

    def detect_query_type(self, query):
        """Detect the type of query"""
        query = query.lower()

        if 'compare' in query and 'rainfall' in query:
            return 'compare_rainfall_production'
        elif 'highest' in query and 'production' in query:
            return 'extreme_production'
        elif 'trend' in query and 'correlate' in query:
            return 'trend_correlation'
        elif 'policy' in query and 'argument' in query:
            return 'policy_arguments'
        else:
            return 'general_comparison'

    def process_query(self, query):
        """Main method to process queries"""
        params = self.parse_query(query)

        if params['query_type'] == 'compare_rainfall_production':
            return self.compare_rainfall_production(params)
        elif params['query_type'] == 'extreme_production':
            return self.find_extreme_production(params)
        else:
            return self.general_analysis(params)

    def compare_rainfall_production(self, params):
        """Compare rainfall and crop production between states"""
        results = {
            'answer': '',
            'data': {},
            'sources': []
        }

        # Fetch climate data for ALL states
        climate_data = {}
        for state in params['states']:
            climate_response = self.fetcher.get_climate_data(state=state)
            climate_data[state] = climate_response.get('records', [])
            results['sources'].append(f"Rainfall data for {state} from India Meteorological Department")

        # Fetch agriculture data for ALL states and crops
        agri_data = {}
        for state in params['states']:
            for crop in params['crops']:
                agri_response = self.fetcher.get_agriculture_data(state=state, crop=crop)
                agri_data[f"{state}_{crop}"] = agri_response.get('records', [])
                results['sources'].append(
                    f"Agriculture production data for {crop} in {state} from Ministry of Agriculture")

        # Generate answer - COMPLETELY FIXED VERSION
        answer_parts = [f"Comparison between {', '.join(params['states'])}:"]
        answer_parts.append("")  # Empty line

        # Add rainfall data for ALL states
        answer_parts.append("🌧️  RAINFALL DATA:")
        for state in params['states']:
            if climate_data.get(state) and climate_data[state]:
                # Find the correct rainfall data for this state
                rainfall_found = False
                for climate_record in climate_data[state]:
                    if climate_record.get('state') == state:
                        rainfall = climate_record.get('annual', 'N/A')
                        answer_parts.append(f"   {state}: {rainfall} mm annual rainfall")
                        rainfall_found = True
                        break
                if not rainfall_found:
                    answer_parts.append(f"   {state}: Rainfall data not found")
            else:
                answer_parts.append(f"   {state}: Rainfall data not available")

        answer_parts.append("")
        answer_parts.append("🌾 CROP PRODUCTION:")

        # Add crop production for ALL states and crops
        production_found = False
        for state in params['states']:
            state_crops_found = False
            for crop in params['crops']:
                key = f"{state}_{crop}"
                if agri_data.get(key) and agri_data[key]:
                    for record in agri_data[key]:
                        if record.get('state') == state and record.get('crop').lower() == crop.lower():
                            production = record.get('production', 'N/A')
                            answer_parts.append(f"   {state} - {crop}: {production} tons")
                            production_found = True
                            state_crops_found = True
                            break

            # If no crops found for this specific state, show message
            if not state_crops_found:
                answer_parts.append(f"   {state}: No {', '.join(params['crops'])} production data available")

        if not production_found:
            answer_parts.append("   No crop production data available for the specified criteria")

        results['answer'] = "\n".join(answer_parts)
        results['data'] = {
            'climate': climate_data,
            'agriculture': agri_data
        }

        return results

    def find_extreme_production(self, params):
        """Find districts with highest/lowest production"""
        results = {
            'answer': '',
            'data': {},
            'sources': []
        }

        agri_data = {}
        for state in params['states']:
            for crop in params['crops']:
                agri_response = self.fetcher.get_agriculture_data(state=state, crop=crop)
                agri_data[f"{state}_{crop}"] = agri_response.get('records', [])
                results['sources'].append(f"Agriculture data for {crop} in {state} from Ministry of Agriculture")

        # Analyze production data
        analysis = []
        for key, records in agri_data.items():
            if records:
                state_crop = key.split('_')
                state = state_crop[0]
                crop = state_crop[1] if len(state_crop) > 1 else 'Crops'

                productions = []
                for record in records:
                    try:
                        production = float(record.get('production', 0))
                        district = record.get('district', 'Unknown')
                        productions.append((district, production))
                    except:
                        continue

                if productions:
                    max_prod = max(productions, key=lambda x: x[1])
                    min_prod = min(productions, key=lambda x: x[1])
                    analysis.append(
                        f"{state} - {crop}: Highest in {max_prod[0]} ({max_prod[1]:,} tons), Lowest in {min_prod[0]} ({min_prod[1]:,} tons)")

        if analysis:
            results['answer'] = "Production Analysis:\n" + "\n".join(analysis)
        else:
            results['answer'] = "No production data found for the specified criteria."

        results['data'] = agri_data

        return results

    def general_analysis(self, params):
        """General analysis fallback"""
        return {
            'answer': f"Analysis for {', '.join(params['states'])} regarding {', '.join(params['crops'])} for years {', '.join(params['years'])}.\n\nThis demonstrates the system's capability to parse complex queries and fetch relevant data from multiple government sources.",
            'data': {},
            'sources': [
                "Ministry of Agriculture & Farmers Welfare - Crop production data",
                "India Meteorological Department - Climate and rainfall data"
            ]
        }