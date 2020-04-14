from query_model import QueryModel
from queries import *


QUERIES = [TRANSMISSION_QUERIES, RISK_FACTORS_QUERIES, VIRUS_GENETIC_QUERIES,
           VACCINES_QUERIES, MEDICAL_CARE_QUERIES, NON_PHARMACEUTICAL_QUERIES, DIAGNOSTICS_QUERIES,
           ETHICAL_QUERIES, INFORMATION_SHARING_QUERIES]

QUERY_NAMES = ['transmission queries', 'risk factors queries', 'virus genetic queries', 'vaccines queries',
               'medical care queries', 'non-pharmaceutical queries', 'diagnostics queries', 'ethical queries',
               'information sharing queries']


def main():
    qm = QueryModel()
    for query_list, query_name in zip(QUERIES, QUERY_NAMES):
        print('\n\n' + query_name + '\n\n')
        for query in query_list:
            print_out = "Query: {}".format(query) + '\n\n'
            hits = qm.query(query)
            for res in hits:
                print_out += '{}:; {} {:3f}'.format(res[0], res[2], res[1]) + '\n'
            print(print_out)


if __name__ == '__main__':
    main()
