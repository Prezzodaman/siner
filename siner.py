import argparse
import wave
import time
import math

parser=argparse.ArgumentParser(description="Finds the sine of each value in a wave file")
parser.add_argument("input_file", type=argparse.FileType("r"),help="The name of the original file")
parser.add_argument("output_file", type=argparse.FileType("w"),help="The name of the sined file")
parser.add_argument("-c", "--cosine", action="store_true", help="Finds the cosine instead")
parser.add_argument("-o", "--offset", type=int, help="Offsets the angle of each byte (degrees)")

args=parser.parse_args()
input_file=args.input_file.name
output_file=args.output_file.name
cosine=args.cosine
angle_offset=args.offset

print("Siner v1.1.0")
print("by Presley Peters, 2023")
print()

success=True
try:
	with wave.open(input_file,"r") as wave_file:
		input_stereo=wave_file.getnchannels()==2
		input_bit_depth=wave_file.getsampwidth()
		input_sample_rate=wave_file.getframerate()
		file_orig=list(wave_file.readframes(wave_file.getnframes()))
	loop_length=len(file_orig)

	if input_stereo:
		if input_bit_depth==1:
			loop_length-=2
		elif input_bit_depth==2:
			loop_length-=4
	else:
		if input_bit_depth==1:
			loop_length-=1
		elif input_bit_depth==2:
			loop_length-=2
except:
	success=False
	print("Error opening input file!")

if success:
	if input_bit_depth>2:
		print("Error: Bit depth not supported!")
	else:
		start_time=time.perf_counter()

		angle_offset/=180/math.pi
		position=0
		print_delay=10000
		while position<loop_length:
			if position%print_delay==0:
				percent=round((position/len(file_orig))*100,2)
				print("Processing... "+str(percent)+"%    ",end="\r")
			if input_bit_depth==1:
				value=((((file_orig[position]+128) & 255)/255)*2*math.pi)+angle_offset
				if cosine:
					byte=math.cos(value)
				else:
					byte=math.sin(value)
				byte=math.floor(byte*128) & 255
				file_orig[position]=byte
				position+=1
			elif input_bit_depth==2:
				byte=((file_orig[position] | (file_orig[position+1]<<8))+32768) & 65535
				value=((byte/65535)*2*math.pi)+angle_offset
				if cosine:
					byte=math.cos(value)
				else:
					byte=math.sin(value)
				byte=math.floor(byte*32768) & 65535

				file_orig[position]=byte & 255
				file_orig[position+1]=byte>>8
				position+=2

		end_time=time.perf_counter()

		with wave.open(output_file,"w") as wave_file:
			if input_stereo:
				wave_file.setnchannels(2)
			else:
				wave_file.setnchannels(1)
			wave_file.setsampwidth(input_bit_depth)
			wave_file.setframerate(input_sample_rate)
			wave_file.writeframesraw(bytearray(file_orig))

		print("Processing... 100.0%    ")
		print("Finished in " + str(round(end_time-start_time,2)) + " seconds!")