# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
import os
import xlsxwriter



def read_file_name(dir):
    # Use a breakpoint in the code line below to debug your script.
    files = os.listdir(dir)
    list_files = []
    for file in files:
        if file.endswith('typo.txt') or file.endswith('typo.ann'):
            list_files.append(os.path.join(dir, file))

    return list_files


def read_records(list_files):
    type_records = dict()
    for file in list_files:
        file_name = file.split("/")[-1].split(".")[0]
        file_open = open(file, 'r')
        for line in file_open:
            if file.endswith(".txt"):
                record = line.strip()
            else:
                record = line.split("\t")[-1].strip()
            if file_name not in type_records.keys():
                type_records[file_name] = [record]
            else:
                temp = type_records[file_name]
                temp.append(record)
                type_records.update({file_name: temp})

    return type_records


def analysis_performance(type_records_gold_standard, type_records_dictionary_lookup, output):
    excel_analysis = os.path.join(output, 'analysis_performance_dictionary_lookup.xlsx')
    workbook_analysis = xlsxwriter.Workbook(excel_analysis)
    all_counter = 0
    all_annotated = 0
    for type, records_gold in type_records_gold_standard.items():
        begin_span = len(type)-31 if len(type) > 31 else 0
        worksheet_analysis = workbook_analysis.add_worksheet(type[begin_span:])
        records_dictionary = type_records_dictionary_lookup.get(type)
        if records_dictionary == None:
            records_dictionary = []
        counter = 0
        for row, record in enumerate(records_gold):
            annotated = "None"
            if record in records_dictionary:
                annotated = 'Annotated'
                counter += 1
            else:
                annotated = 'Not Annotated'

            worksheet_analysis.write(row, 0, record)
            worksheet_analysis.write(row, 1, annotated)

        worksheet_analysis.write(0, 3, "Accuracy")
        worksheet_analysis.write(0, 4, counter/len(records_gold))
        all_counter +=  len(records_gold)
        all_annotated += counter

    workbook_analysis.close()
    print(all_annotated/all_counter)
    print(all_annotated)
    print(all_counter)




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="performance checker")
    parser.add_argument('--gold_standard', help='Gold Standard files of typos')
    parser.add_argument('--dictionary_lookup', help='Output of fuzzy dictionary lookup')
    parser.add_argument('--output', help='analysis of performance of fuzzy dictionary lookup')

    args = parser.parse_args()

    gold_standard = args.gold_standard
    dictionary_lookup = args.dictionary_lookup
    output = args.output

    list_files_gold_standard = read_file_name(gold_standard)
    type_records_gold_standard = read_records(list_files_gold_standard)

    list_files_dictionary_lookup = read_file_name(dictionary_lookup)
    type_records_dictionary_lookup = read_records(list_files_dictionary_lookup)

    analysis_performance(type_records_gold_standard, type_records_dictionary_lookup, output)








# See PyCharm help at https://www.jetbrains.com/help/pycharm/
