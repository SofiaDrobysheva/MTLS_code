from Bio import SeqIO as sq
import sys
import argparse

start=['ATG','GUG','UUG']
stop=['TAG','TGA','TAA']

def orf_finder(seq, min_length=290):
	a=-2
	b=-2
	c=-2
	
	start_cods=[]
	
	start=0
	start_ty=0
	while a!=-1:
		a=seq.find('ATG',start)
		frame=a%3
		start=a+3
		start_cods.append([a,start_ty,frame])
	

	start=0
	start_ty=1
	while b!=-1:
		b=seq.find('GTG',start)
		frame=b%3
		start=b+3
		start_cods.append([b,start_ty,frame])

	start=0
	start_ty=2
	while c!=-1:
		c=seq.find('TTG',start)
		frame=c%3
		start=c+3
		start_cods.append([c,start_ty,frame])
	

	a=-2
	b=-2
	c=-2
	
	stop_cods=[]
	
	start=0
	while a!=-1:
		a=seq.find('TAG',start)
		frame=a%3
		start=a+3
		stop_cods.append([a,frame])
	

	start=0
	while b!=-1:
		b=seq.find('TGA',start)
		frame=b%3
		start=b+3
		stop_cods.append([b,frame])

	start=0
	while c!=-1:
		c=seq.find('TAA',start)
		frame=c%3
		start=c+3
		stop_cods.append([c,frame])


	start_f=[i for i in start_cods if i[2]==0]
	start_f=sorted(start_f,key=lambda x:x[0])
	start_s=[i for i in start_cods if i[2]==1]
	start_s=sorted(start_s,key=lambda x:x[0])
	start_t=[i for i in start_cods if i[2]==2]
	start_t=sorted(start_t,key=lambda x:x[0])

	stop_f=[i for i in stop_cods if i[1]==0]
	stop_f=sorted(stop_f,key=lambda x:x[0])
	stop_s=[i for i in stop_cods if i[1]==1]
	stop_s=sorted(stop_s,key=lambda x:x[0])
	stop_t=[i for i in stop_cods if i[1]==2]
	stop_t=sorted(stop_t,key=lambda x:x[0])

	j=0
	frames_f=[]
	end=False
	for i in start_f:
		while i[0]>stop_f[j][0]:
			j+=1
			if j>=len(stop_f):
				end=True
				break
						
		if j<len(stop_f):
			frames_f.append([i[0],stop_f[j][0],i[1]])
		if end==True:
			break
	
	frames_f=[i for i in frames_f if (i[1]-i[0]>min_length)]

	j=0
	frames_s=[]
	end=False
	for i in start_s:
		while i[0]>stop_s[j][0]:
			j+=1
			if j>=len(stop_s):
				end=True
				break
						
		if j<len(stop_s):
			frames_s.append([i[0],stop_s[j][0],i[1]])
		if end==True:
			break
	
	frames_s=[i for i in frames_s if (i[1]-i[0]>min_length)]

	j=0
	frames_t=[]
	end=False
	for i in start_t:
		while i[0]>stop_t[j][0]:
			j+=1
			if j>=len(stop_t):
				end=True
				break
						
		if j<len(stop_t):
			frames_t.append([i[0],stop_t[j][0],i[1]])
		if end==True:
			break
	
	frames_t=[i for i in frames_t if (i[1]-i[0]>min_length)]

	total_frames=[]
	for i in frames_f:
		total_frames.append(i)
	
	for i in frames_s:
		total_frames.append(i)

	for i in frames_t:
		total_frames.append(i)

	total_frames=sorted(total_frames,key=lambda x:x[0])

	return total_frames



def gcContent(seq):
	gc=seq.count('G')+seq.count('C')
	
	return gc/len(seq)


def scorer(seq,orfs):
	for i,orf in enumerate(orfs):
		start=orf[0]
		end=orf[1]+3
		type_st=orf[2]
		stri=seq[start:end]
		gc=gcContent(stri)
		if type_st==0:
			multiplier=0.83
		elif type_st==1:
			multiplier=0.14
		else:
			multiplier=0.03
		if gc>0.8 or gc<0.3:
			gc=0
		orfs[i].append(len(stri)*gc*multiplier)
		orfs[i].append(i)
	return orfs

def overlap_network(orfs):
	empty_placeholder=[orfs[len(orfs)-1][1]+1,-1,-1,-1]
	orfs.append(empty_placeholder)
	network={}
	for i, orf in enumerate(orfs):
		if i>= len(orfs)-2: break
		if orf[4] not in network:
			network[orf[4]]=set()
		j=i
		while orfs[j+1][0]<=orfs[j][1]:
			network[orf[4]].add(orfs[j+1][4])
			if orfs[j+1][4] not in network:
				network[orfs[j+1][4]]=set()
			network[orfs[j+1][4]].add(orf[4])
			j+=1
	
	return network


def solve_overlap(orfs, network):
	orfs=sorted(orfs,key=lambda x:x[3])
	orfs.reverse()
	orfs.pop()
	final=[]
	a=0
	for key, value in network.items():
		network[key]=list(value)
	for orf in orfs:
		print(a)
		a+=1
		if orf[4] in network:
			if bool(network[orf[4]])==False:
				final.append(orf)
				network.pop(orf[4])
			elif bool(network[orf[4]])==True:
				final.append(orf)
				to_pop=[]
				for i in network[orf[4]]:
					to_pop.append(i)
				for j in to_pop:
					if j in network:
						network.pop(j)
				network.pop(orf[4])
	final=[i for i in final if i[3]>0]
	
	return final, network

def main(args):
	#parse sequence and make it uppercase
	sequences=[]
	for sequence in sq.parse(args.input,"fasta"):
		sequence.seq=sequence.seq.upper()
		sequences.append(sequence)

	sequence=sequences[0].seq
	reverse_complement=sequence.reverse_complement()

	#raise exception if file contains more than one sequence
	try:
		if len(sequences)>1:
			raise IndexError
	except IndexError:
		print("The file contains more than one sequence")
		sys.exit(1)

	#analyze positive strand
	orfs_pos=scorer(sequence, orf_finder(sequence))
	network_pos=overlap_network(orfs_pos)
	final_pos, sec_net=solve_overlap(orfs_pos,network_pos)

	#analyze negative strand
	orfs_neg=scorer(reverse_complement, orf_finder(reverse_complement))
	network_neg=overlap_network(orfs_neg)
	final_neg, sec_net=solve_overlap(orfs_neg,network_neg)

	for i in final_pos:
		i[2]=True

	length=len(sequence)

	for i in final_neg:
		i[2]=False

	final=final_pos+final_neg
	final=sorted(final, key=lambda x:x[0])

	with open(args.output,"w") as f:
		for i,v  in enumerate(final):
			if v[2]==True:
				f.write(">orf{} | score {}\n".format(i,v[3]))
				f.write("{}\n".format(sequence[v[0]:(v[1])].translate()))
			elif v[2]==False:
				f.write(">orf{}_rev | score {}\n".format(i,v[3]))
				f.write("{}\n".format(reverse_complement[v[0]:(v[1])].translate()))
	

	print(len(final))

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description="Takes a genome as input and extracts ORFs out of it.", formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("input", type=str, help="path or name of input fasta file")
    parser.add_argument("-o","--output", type=str, help="path or name of the output multifasta file", default="out.mfa")
    
    args = parser.parse_args()

    main(args)