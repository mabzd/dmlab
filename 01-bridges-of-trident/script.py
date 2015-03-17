import Orange

def print_instance(instance):
	for attribute in instance:
		print "{0:<10}'{1}'".format(attribute.variable.name, attribute.value)

def print_instances(instances):
	for instance in instances:
		print_instance(instance)
		print

def print_table_info(table):
	format_line = "{0:<3} {1:<10} {2:<12} {3:<10} {4:<10}"
	print format_line.format("No", "Variable", "Type", "Avg/modal", "Unknown")
	for i, attribute in enumerate(table.domain):
		print format_line.format(
			i+1,
			attribute.name,
			str(attribute.var_type),
			calc_average_or_modal(table, attribute),
			count_special(table, attribute))

def print_attribute_histogram(table, attribute):
	histogram = create_histogram(table, attribute)
	total = sum(histogram.values())
	for key, value in histogram.iteritems():
		print "{0:<10} {1:<5} {2:.2f}%".format(key, value, float(value)/total*100)

def calc_average(table, attribute):
	values = [instance[attribute] for instance in table if not instance[attribute].is_special()]
	return sum(values) / float(len(values))

def calc_modal(table, attribute):
	histogram = create_histogram(table, attribute)
	return max(histogram, key=histogram.get)

def calc_average_or_modal(table, attribute):
	avg_modal = None
	if attribute.var_type == Orange.feature.Type.Continuous:
		avg_modal = round(calc_average(table, attribute), 2)
	elif attribute.var_type == Orange.feature.Type.Discrete:
		avg_modal = calc_modal(table, attribute)
	return avg_modal

def count_special(table, attribute):
	return sum([1 for instance in table if instance[attribute].is_special()])

def create_histogram(table, attribute):
	histogram = {value: 0 for value in attribute.values}
	for instance in table:
		if not instance[attribute].is_special():
			histogram[instance[attribute].value] += 1
	return histogram

def random_instances(table, n):
	for i in range(0, n):
		yield table.random_instance()

table = Orange.data.Table("bridges.tab")

instances = random_instances(table, 3)
print_instances(instances)

if table.domain.class_var != None:
	print "Histogram for class attribute: {}".format(table.domain.class_var.name)
	print_attribute_histogram(table, table.domain.class_var)

print "\nAttributes count: {}".format(len(table.domain))
print_table_info(table)

