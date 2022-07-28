from Bio import SeqIO as sq
import argparse


def main(args):
	
	predicted=[]
	for sequence in sq.parse(args.input_predicted,"fasta"):
		sequence.seq=sequence.seq.upper()
		predicted.append(sequence)
	
	glimmer=[]
	for sequence in sq.parse(args.input_glimmer,"fasta"):
		sequence.seq=sequence.seq.upper()
		glimmer.append(sequence)
	
	references=[]
	for sequence in sq.parse(args.input_reference,"fasta"):
		sequence.seq=sequence.seq.upper()
		references.append(sequence)
	
	predicted_set=set()
	for sequence in predicted:
		predicted_set.add(sequence.seq)
	glimmer_set=set()
	for sequence in glimmer:
		glimmer_set.add(sequence.seq)
	reference_set=set()
	for sequence in references:
		reference_set.add(sequence.seq)
	
	pred_fn=0
	for true_pos in reference_set:
		if true_pos not in predicted_set:
			pred_fn+=1
	pred_tp=len(reference_set.intersection(predicted_set))
	pred_fp=abs(len(predicted_set) - len(reference_set))
	pred_sensitivity=(pred_tp/(pred_tp+pred_fn))*100
	pred_posval=(pred_tp/(pred_tp+pred_fp))*100

	glimm_fn=0
	for true_pos in reference_set:
		if true_pos not in glimmer_set:
			glimm_fn+=1
	glimm_tp=len(reference_set.intersection(glimmer_set))
	glimm_fp=abs(len(glimmer_set) - len(reference_set))
	glimm_sensitivity=(glimm_tp/(glimm_tp+glimm_fn))*100
	glimm_posval=(glimm_tp/(glimm_tp+glimm_fp))*100

	print("Our Predictor:\nPredicted: {} sequences\nFN: {}\tTP: {}\tFP:{}\n\nThe Positive predictive value is of: {:.2f}%\n\nThe sensitivity is: {:.2f}%".format(len(predicted_set),pred_fn,pred_tp,pred_fp,pred_posval,pred_sensitivity))
	# print()
	# print([pred_fn,pred_fp,pred_tp])

	print("Glimmer:\nPredicted: {} sequences\nFN: {}\tTP: {}\tFP:{}\n\nThe Positive prediictive value is of: {:.2f}%\n\nThe sensitivity is: {:.2f}%".format(len(glimmer_set),glimm_fn,glimm_tp,glimm_fp,glimm_posval,glimm_sensitivity))

	print("\nThe length of the reference set is: {}".format(len(reference_set)))



if __name__ =='__main__':
	parser = argparse.ArgumentParser(description="By taking as input two predicted proteomes and a reference one outputs statistics on the first two inputs", formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("input_predicted", type=str, help="path or name of input fasta file (Predictor output)")
	parser.add_argument("input_glimmer", type=str, help="path or name of input fasta file (GLIMMER output)")
	parser.add_argument("input_reference", type=str, help="path or name of input fasta file (Reference proteome)")
	parser.add_argument("-o","--output", type=str, help="path or name of the output file", default="stts.txt")
	
	args = parser.parse_args()

	main(args)