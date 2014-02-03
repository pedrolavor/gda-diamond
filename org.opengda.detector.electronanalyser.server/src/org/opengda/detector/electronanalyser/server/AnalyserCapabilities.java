/*-
 * Copyright © 2012 Diamond Light Source Ltd.
 *
 * This file is part of GDA.
 *
 * GDA is free software: you can redistribute it and/or modify it under the
 * terms of the GNU General Public License version 3 as published by the Free
 * Software Foundation.
 *
 * GDA is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
 * FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
 * details.
 *
 * You should have received a copy of the GNU General Public License along
 * with GDA. If not, see <http://www.gnu.org/licenses/>.
 */

package org.opengda.detector.electronanalyser.server;

import gda.factory.Findable;

import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;

//import org.apache.commons.lang.ArrayUtils;

import uk.ac.diamond.scisoft.analysis.dataset.AbstractDataset;
import uk.ac.diamond.scisoft.analysis.dataset.DoubleDataset;

public class AnalyserCapabilities implements Findable {

	private String name = "AnalyserCapabilties";
	
	private Map<String, double[]> lens2angles = new HashMap<String, double[]>(8);
	
	public AnalyserCapabilities() {
		for(Object[] o: new Object[][] {
											{"Transmission",
												new double[] {
													1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,263,264,265,266,267,268,269,270,271,272,273,274,275,276,277,278,279,280,281,282,283,284,285,286,287,288,289,290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,311,312,313,314,315,316,317,318,319,320,321,322,323,324,325,326,327,328,329,330,331,332,333,334,335,336,337,338,339,340,341,342,343,344,345,346,347,348,349,350,351,352,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375,376,377,378,379,380,381,382,383,384,385,386,387,388,389,390,391,392,393,394,395,396,397,398,399,400,401,402,403,404,405,406,407,408,409,410,411,412,413,414,415,416,417,418,419,420,421,422,423,424,425,426,427,428,429,430,431,432,433,434,435,436,437,438,439,440,441,442,443,444,445,446,447,448,449,450,451,452,453,454,455,456,457,458,459,460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495,496,497,498,499,500,501,502,503,504,505,506,507,508,509,510,511,512,513,514,515,516,517,518,519,520,521,522,523,524,525,526,527,528,529,530,531,532,533,534,535,536,537,538,539,540,541,542,543,544,545,546,547,548,549,550,551,552,553,554,555,556,557,558,559,560,561,562,563,564,565,566,567,568,569,570,571,572,573,574,575,576,577,578,579,580,581,582,583,584,585,586,587,588,589,590,591,592,593,594,595,596,597,598,599,600,601,602,603,604,605,606,607,608,609,610,611,612,613,614,615,616,617,618,619,620,621,622,623,624,625,626,627,628,629,630,631,632,633,634,635,636,637,638,639,640,641,642,643,644,645,646,647,648,649,650,651,652,653,654,655,656,657,658,659,660,661,662,663,664,665,666,667,668,669,670,671,672,673,674,675,676,677,678,679,680,681,682,683,684,685,686,687,688,689,690,691,692,693,694,695,696,697,698,699,700,701,702,703,704,705,706,707,708,709,710,711,712,713,714,715,716,717,718,719,720,721,722,723,724,725,726,727,728,729,730,731,732,733,734,735,736,737,738,739,740,741,742,743,744,745,746,747,748,749,750,751,752,753,754,755,756,757,758,759,760,761,762,763,764,765,766,767,768,769,770,771,772,773,774,775,776,777,778,779,780,781,782,783,784,785,786,787,788,789,790,791,792,793,794,795,796,797,798,799,800,801,802,803,804,805,806,807,808,809,810,811,812,813,814,815,816,817,818,819,820,821,822,823,824,825,826,827,828,829,830,831,832,833,834,835,836,837,838,839,840,841,842,843,844,845,846,847,848,849,850,851,852,853,854,855,856,857,858,859,860,861,862,863,864,865,866,867,868,869,870,871,872,873,874,875,876,877,878,879,880,881,882,883,884,885,886,887,888,889,890,891,892,893,894,895,896,897,898,899,900
												}
											},
											{"Angular45", 
												new double[] {
													-26.82561, -26.76599, -26.70638, -26.64677, -26.58716, -26.52754, -26.46793, -26.40832, -26.34871, -26.28909, -26.22948, -26.16987, -26.11026, -26.05064, -25.99103, -25.93142, -25.87181, -25.81219, -25.75258, -25.69297, -25.63336, -25.57374, -25.51413, -25.45452, -25.39491, -25.33530, -25.27568, -25.21607, -25.15646, -25.09685, -25.03723, -24.97762, -24.91801, -24.85840, -24.79878, -24.73917, -24.67956, -24.61995, -24.56033, -24.50072, -24.44111, -24.38150, -24.32188, -24.26227, -24.20266, -24.14305, -24.08343, -24.02382, -23.96421, -23.90460, -23.84498, -23.78537, -23.72576, -23.66615, -23.60653, -23.54692, -23.48731, -23.42770, -23.36808, -23.30847, -23.24886, -23.18925, -23.12963, -23.07002, -23.01041, -22.95080, -22.89118, -22.83157, -22.77196, -22.71235, -22.65273, -22.59312, -22.53351, -22.47390, -22.41428, -22.35467, -22.29506, -22.23545, -22.17583, -22.11622, -22.05661, -21.99700, -21.93738, -21.87777, -21.81816, -21.75855, -21.69894, -21.63932, -21.57971, -21.52010, -21.46049, -21.40087, -21.34126, -21.28165, -21.22204, -21.16242, -21.10281, -21.04320, -20.98359, -20.92397, -20.86436, -20.80475, -20.74514, -20.68552, -20.62591, -20.56630, -20.50669, -20.44707, -20.38746, -20.32785, -20.26824, -20.20862, -20.14901, -20.08940, -20.02979, -19.97017, -19.91056, -19.85095, -19.79134, -19.73172, -19.67211, -19.61250, -19.55289, -19.49327, -19.43366, -19.37405, -19.31444, -19.25482, -19.19521, -19.13560, -19.07599, -19.01637, -18.95676, -18.89715, -18.83754, -18.77792, -18.71831, -18.65870, -18.59909, -18.53947, -18.47986, -18.42025, -18.36064, -18.30102, -18.24141, -18.18180, -18.12219, -18.06258, -18.00296, -17.94335, -17.88374, -17.82413, -17.76451, -17.70490, -17.64529, -17.58568, -17.52606, -17.46645, -17.40684, -17.34723, -17.28761, -17.22800, -17.16839, -17.10878, -17.04916, -16.98955, -16.92994, -16.87033, -16.81071, -16.75110, -16.69149, -16.63188, -16.57226, -16.51265, -16.45304, -16.39343, -16.33381, -16.27420, -16.21459, -16.15498, -16.09536, -16.03575, -15.97614, -15.91653, -15.85691, -15.79730, -15.73769, -15.67808, -15.61846, -15.55885, -15.49924, -15.43963, -15.38001, -15.32040, -15.26079, -15.20118, -15.14156, -15.08195, -15.02234, -14.96273, -14.90311, -14.84350, -14.78389, -14.72428, -14.66466, -14.60505, -14.54544, -14.48583, -14.42622, -14.36660, -14.30699, -14.24738, -14.18777, -14.12815, -14.06854, -14.00893, -13.94932, -13.88970, -13.83009, -13.77048, -13.71087, -13.65125, -13.59164, -13.53203, -13.47242, -13.41280, -13.35319, -13.29358, -13.23397, -13.17435, -13.11474, -13.05513, -12.99552, -12.93590, -12.87629, -12.81668, -12.75707, -12.69745, -12.63784, -12.57823, -12.51862, -12.45900, -12.39939, -12.33978, -12.28017, -12.22055, -12.16094, -12.10133, -12.04172, -11.98210, -11.92249, -11.86288, -11.80327, -11.74365, -11.68404, -11.62443, -11.56482, -11.50520, -11.44559, -11.38598, -11.32637, -11.26675, -11.20714, -11.14753, -11.08792, -11.02830, -10.96869, -10.90908, -10.84947, -10.78986, -10.73024, -10.67063, -10.61102, -10.55141, -10.49179, -10.43218, -10.37257, -10.31296, -10.25334, -10.19373, -10.13412, -10.07451, -10.01489, -9.95528, -9.89567, -9.83606, -9.77644, -9.71683, -9.65722, -9.59761, -9.53799, -9.47838, -9.41877, -9.35916, -9.29954, -9.23993, -9.18032, -9.12071, -9.06109, -9.00148, -8.94187, -8.88226, -8.82264, -8.76303, -8.70342, -8.64381, -8.58419, -8.52458, -8.46497, -8.40536, -8.34574, -8.28613, -8.22652, -8.16691, -8.10729, -8.04768, -7.98807, -7.92846, -7.86884, -7.80923, -7.74962, -7.69001, -7.63039, -7.57078, -7.51117, -7.45156, -7.39194, -7.33233, -7.27272, -7.21311, -7.15350, -7.09388, -7.03427, -6.97466, -6.91505, -6.85543, -6.79582, -6.73621, -6.67660, -6.61698, -6.55737, -6.49776, -6.43815, -6.37853, -6.31892, -6.25931, -6.19970, -6.14008, -6.08047, -6.02086, -5.96125, -5.90163, -5.84202, -5.78241, -5.72280, -5.66318, -5.60357, -5.54396, -5.48435, -5.42473, -5.36512, -5.30551, -5.24590, -5.18628, -5.12667, -5.06706, -5.00745, -4.94783, -4.88822, -4.82861, -4.76900, -4.70938, -4.64977, -4.59016, -4.53055, -4.47093, -4.41132, -4.35171, -4.29210, -4.23248, -4.17287, -4.11326, -4.05365, -3.99403, -3.93442, -3.87481, -3.81520, -3.75558, -3.69597, -3.63636, -3.57675, -3.51714, -3.45752, -3.39791, -3.33830, -3.27869, -3.21907, -3.15946, -3.09985, -3.04024, -2.98062, -2.92101, -2.86140, -2.80179, -2.74217, -2.68256, -2.62295, -2.56334, -2.50372, -2.44411, -2.38450, -2.32489, -2.26527, -2.20566, -2.14605, -2.08644, -2.02682, -1.96721, -1.90760, -1.84799, -1.78837, -1.72876, -1.66915, -1.60954, -1.54992, -1.49031, -1.43070, -1.37109, -1.31147, -1.25186, -1.19225, -1.13264, -1.07302, -1.01341, -0.95380, -0.89419, -0.83457, -0.77496, -0.71535, -0.65574, -0.59612, -0.53651, -0.47690, -0.41729, -0.35767, -0.29806, -0.23845, -0.17884, -0.11922, -0.05961, 0.00000, 0.05961, 0.11922, 0.17884, 0.23845, 0.29806, 0.35767, 0.41729, 0.47690, 0.53651, 0.59612, 0.65574, 0.71535, 0.77496, 0.83457, 0.89419, 0.95380, 1.01341, 1.07302, 1.13264, 1.19225, 1.25186, 1.31147, 1.37109, 1.43070, 1.49031, 1.54992, 1.60954, 1.66915, 1.72876, 1.78837, 1.84799, 1.90760, 1.96721, 2.02682, 2.08644, 2.14605, 2.20566, 2.26527, 2.32489, 2.38450, 2.44411, 2.50372, 2.56334, 2.62295, 2.68256, 2.74217, 2.80179, 2.86140, 2.92101, 2.98062, 3.04024, 3.09985, 3.15946, 3.21907, 3.27869, 3.33830, 3.39791, 3.45752, 3.51714, 3.57675, 3.63636, 3.69597, 3.75558, 3.81520, 3.87481, 3.93442, 3.99403, 4.05365, 4.11326, 4.17287, 4.23248, 4.29210, 4.35171, 4.41132, 4.47093, 4.53055, 4.59016, 4.64977, 4.70938, 4.76900, 4.82861, 4.88822, 4.94783, 5.00745, 5.06706, 5.12667, 5.18628, 5.24590, 5.30551, 5.36512, 5.42473, 5.48435, 5.54396, 5.60357, 5.66318, 5.72280, 5.78241, 5.84202, 5.90163, 5.96125, 6.02086, 6.08047, 6.14008, 6.19970, 6.25931, 6.31892, 6.37853, 6.43815, 6.49776, 6.55737, 6.61698, 6.67660, 6.73621, 6.79582, 6.85543, 6.91505, 6.97466, 7.03427, 7.09388, 7.15350, 7.21311, 7.27272, 7.33233, 7.39194, 7.45156, 7.51117, 7.57078, 7.63039, 7.69001, 7.74962, 7.80923, 7.86884, 7.92846, 7.98807, 8.04768, 8.10729, 8.16691, 8.22652, 8.28613, 8.34574, 8.40536, 8.46497, 8.52458, 8.58419, 8.64381, 8.70342, 8.76303, 8.82264, 8.88226, 8.94187, 9.00148, 9.06109, 9.12071, 9.18032, 9.23993, 9.29954, 9.35916, 9.41877, 9.47838, 9.53799, 9.59761, 9.65722, 9.71683, 9.77644, 9.83606, 9.89567, 9.95528, 10.01489, 10.07451, 10.13412, 10.19373, 10.25334, 10.31296, 10.37257, 10.43218, 10.49179, 10.55141, 10.61102, 10.67063, 10.73024, 10.78986, 10.84947, 10.90908, 10.96869, 11.02830, 11.08792, 11.14753, 11.20714, 11.26675, 11.32637, 11.38598, 11.44559, 11.50520, 11.56482, 11.62443, 11.68404, 11.74365, 11.80327, 11.86288, 11.92249, 11.98210, 12.04172, 12.10133, 12.16094, 12.22055, 12.28017, 12.33978, 12.39939, 12.45900, 12.51862, 12.57823, 12.63784, 12.69745, 12.75707, 12.81668, 12.87629, 12.93590, 12.99552, 13.05513, 13.11474, 13.17435, 13.23397, 13.29358, 13.35319, 13.41280, 13.47242, 13.53203, 13.59164, 13.65125, 13.71087, 13.77048, 13.83009, 13.88970, 13.94932, 14.00893, 14.06854, 14.12815, 14.18777, 14.24738, 14.30699, 14.36660, 14.42622, 14.48583, 14.54544, 14.60505, 14.66466, 14.72428, 14.78389, 14.84350, 14.90311, 14.96273, 15.02234, 15.08195, 15.14156, 15.20118, 15.26079, 15.32040, 15.38001, 15.43963, 15.49924, 15.55885, 15.61846, 15.67808, 15.73769, 15.79730, 15.85691, 15.91653, 15.97614, 16.03575, 16.09536, 16.15498, 16.21459, 16.27420, 16.33381, 16.39343, 16.45304, 16.51265, 16.57226, 16.63188, 16.69149, 16.75110, 16.81071, 16.87033, 16.92994, 16.98955, 17.04916, 17.10878, 17.16839, 17.22800, 17.28761, 17.34723, 17.40684, 17.46645, 17.52606, 17.58568, 17.64529, 17.70490, 17.76451, 17.82413, 17.88374, 17.94335, 18.00296, 18.06258, 18.12219, 18.18180, 18.24141, 18.30102, 18.36064, 18.42025, 18.47986, 18.53947, 18.59909, 18.65870, 18.71831, 18.77792, 18.83754, 18.89715, 18.95676, 19.01637, 19.07599, 19.13560, 19.19521, 19.25482, 19.31444, 19.37405, 19.43366, 19.49327, 19.55289, 19.61250, 19.67211, 19.73172, 19.79134, 19.85095, 19.91056, 19.97017, 20.02979, 20.08940, 20.14901, 20.20862, 20.26824, 20.32785, 20.38746, 20.44707, 20.50669, 20.56630, 20.62591, 20.68552, 20.74514, 20.80475, 20.86436, 20.92397, 20.98359, 21.04320, 21.10281, 21.16242, 21.22204, 21.28165, 21.34126, 21.40087, 21.46049, 21.52010, 21.57971, 21.63932, 21.69894, 21.75855, 21.81816, 21.87777, 21.93738, 21.99700, 22.05661, 22.11622, 22.17583, 22.23545, 22.29506, 22.35467, 22.41428, 22.47390, 22.53351, 22.59312, 22.65273, 22.71235, 22.77196, 22.83157, 22.89118, 22.95080, 23.01041, 23.07002, 23.12963, 23.18925, 23.24886, 23.30847, 23.36808, 23.42770, 23.48731, 23.54692, 23.60653, 23.66615, 23.72576, 23.78537, 23.84498, 23.90460, 23.96421, 24.02382, 24.08343, 24.14305, 24.20266, 24.26227, 24.32188, 24.38150, 24.44111, 24.50072, 24.56033, 24.61995, 24.67956, 24.73917, 24.79878, 24.85840, 24.91801, 24.97762, 25.03723, 25.09685, 25.15646, 25.21607, 25.27568, 25.33530, 25.39491, 25.45452, 25.51413, 25.57374, 25.63336, 25.69297, 25.75258, 25.81219, 25.87181, 25.93142, 25.99103, 26.05064, 26.11026, 26.16987, 26.22948, 26.28909, 26.34871, 26.40832, 26.46793, 26.52754, 26.58716, 26.64677, 26.70638, 26.76599
												}
											},
											{"Angular60", 
												new double[] {
													-34.81621, -34.73884, -34.66147, -34.58410, -34.50674, -34.42937, -34.35200, -34.27463, -34.19726, -34.11989, -34.04252, -33.96515, -33.88778, -33.81041, -33.73304, -33.65567, -33.57830, -33.50093, -33.42356, -33.34619, -33.26883, -33.19146, -33.11409, -33.03672, -32.95935, -32.88198, -32.80461, -32.72724, -32.64987, -32.57250, -32.49513, -32.41776, -32.34039, -32.26302, -32.18565, -32.10829, -32.03092, -31.95355, -31.87618, -31.79881, -31.72144, -31.64407, -31.56670, -31.48933, -31.41196, -31.33459, -31.25722, -31.17985, -31.10248, -31.02511, -30.94774, -30.87038, -30.79301, -30.71564, -30.63827, -30.56090, -30.48353, -30.40616, -30.32879, -30.25142, -30.17405, -30.09668, -30.01931, -29.94194, -29.86457, -29.78720, -29.70983, -29.63247, -29.55510, -29.47773, -29.40036, -29.32299, -29.24562, -29.16825, -29.09088, -29.01351, -28.93614, -28.85877, -28.78140, -28.70403, -28.62666, -28.54929, -28.47193, -28.39456, -28.31719, -28.23982, -28.16245, -28.08508, -28.00771, -27.93034, -27.85297, -27.77560, -27.69823, -27.62086, -27.54349, -27.46612, -27.38875, -27.31138, -27.23402, -27.15665, -27.07928, -27.00191, -26.92454, -26.84717, -26.76980, -26.69243, -26.61506, -26.53769, -26.46032, -26.38295, -26.30558, -26.22821, -26.15084, -26.07347, -25.99611, -25.91874, -25.84137, -25.76400, -25.68663, -25.60926, -25.53189, -25.45452, -25.37715, -25.29978, -25.22241, -25.14504, -25.06767, -24.99030, -24.91293, -24.83557, -24.75820, -24.68083, -24.60346, -24.52609, -24.44872, -24.37135, -24.29398, -24.21661, -24.13924, -24.06187, -23.98450, -23.90713, -23.82976, -23.75239, -23.67502, -23.59766, -23.52029, -23.44292, -23.36555, -23.28818, -23.21081, -23.13344, -23.05607, -22.97870, -22.90133, -22.82396, -22.74659, -22.66922, -22.59185, -22.51448, -22.43711, -22.35975, -22.28238, -22.20501, -22.12764, -22.05027, -21.97290, -21.89553, -21.81816, -21.74079, -21.66342, -21.58605, -21.50868, -21.43131, -21.35394, -21.27657, -21.19921, -21.12184, -21.04447, -20.96710, -20.88973, -20.81236, -20.73499, -20.65762, -20.58025, -20.50288, -20.42551, -20.34814, -20.27077, -20.19340, -20.11603, -20.03866, -19.96130, -19.88393, -19.80656, -19.72919, -19.65182, -19.57445, -19.49708, -19.41971, -19.34234, -19.26497, -19.18760, -19.11023, -19.03286, -18.95549, -18.87812, -18.80075, -18.72339, -18.64602, -18.56865, -18.49128, -18.41391, -18.33654, -18.25917, -18.18180, -18.10443, -18.02706, -17.94969, -17.87232, -17.79495, -17.71758, -17.64021, -17.56285, -17.48548, -17.40811, -17.33074, -17.25337, -17.17600, -17.09863, -17.02126, -16.94389, -16.86652, -16.78915, -16.71178, -16.63441, -16.55704, -16.47967, -16.40230, -16.32494, -16.24757, -16.17020, -16.09283, -16.01546, -15.93809, -15.86072, -15.78335, -15.70598, -15.62861, -15.55124, -15.47387, -15.39650, -15.31913, -15.24176, -15.16439, -15.08703, -15.00966, -14.93229, -14.85492, -14.77755, -14.70018, -14.62281, -14.54544, -14.46807, -14.39070, -14.31333, -14.23596, -14.15859, -14.08122, -14.00385, -13.92649, -13.84912, -13.77175, -13.69438, -13.61701, -13.53964, -13.46227, -13.38490, -13.30753, -13.23016, -13.15279, -13.07542, -12.99805, -12.92068, -12.84331, -12.76594, -12.68858, -12.61121, -12.53384, -12.45647, -12.37910, -12.30173, -12.22436, -12.14699, -12.06962, -11.99225, -11.91488, -11.83751, -11.76014, -11.68277, -11.60540, -11.52803, -11.45067, -11.37330, -11.29593, -11.21856, -11.14119, -11.06382, -10.98645, -10.90908, -10.83171, -10.75434, -10.67697, -10.59960, -10.52223, -10.44486, -10.36749, -10.29013, -10.21276, -10.13539, -10.05802, -9.98065, -9.90328, -9.82591, -9.74854, -9.67117, -9.59380, -9.51643, -9.43906, -9.36169, -9.28432, -9.20695, -9.12958, -9.05222, -8.97485, -8.89748, -8.82011, -8.74274, -8.66537, -8.58800, -8.51063, -8.43326, -8.35589, -8.27852, -8.20115, -8.12378, -8.04641, -7.96904, -7.89167, -7.81431, -7.73694, -7.65957, -7.58220, -7.50483, -7.42746, -7.35009, -7.27272, -7.19535, -7.11798, -7.04061, -6.96324, -6.88587, -6.80850, -6.73113, -6.65377, -6.57640, -6.49903, -6.42166, -6.34429, -6.26692, -6.18955, -6.11218, -6.03481, -5.95744, -5.88007, -5.80270, -5.72533, -5.64796, -5.57059, -5.49322, -5.41586, -5.33849, -5.26112, -5.18375, -5.10638, -5.02901, -4.95164, -4.87427, -4.79690, -4.71953, -4.64216, -4.56479, -4.48742, -4.41005, -4.33268, -4.25531, -4.17795, -4.10058, -4.02321, -3.94584, -3.86847, -3.79110, -3.71373, -3.63636, -3.55899, -3.48162, -3.40425, -3.32688, -3.24951, -3.17214, -3.09477, -3.01741, -2.94004, -2.86267, -2.78530, -2.70793, -2.63056, -2.55319, -2.47582, -2.39845, -2.32108, -2.24371, -2.16634, -2.08897, -2.01160, -1.93423, -1.85686, -1.77950, -1.70213, -1.62476, -1.54739, -1.47002, -1.39265, -1.31528, -1.23791, -1.16054, -1.08317, -1.00580, -0.92843, -0.85106, -0.77369, -0.69632, -0.61895, -0.54159, -0.46422, -0.38685, -0.30948, -0.23211, -0.15474, -0.07737, 0.00000, 0.07737, 0.15474, 0.23211, 0.30948, 0.38685, 0.46422, 0.54159, 0.61895, 0.69632, 0.77369, 0.85106, 0.92843, 1.00580, 1.08317, 1.16054, 1.23791, 1.31528, 1.39265, 1.47002, 1.54739, 1.62476, 1.70213, 1.77950, 1.85686, 1.93423, 2.01160, 2.08897, 2.16634, 2.24371, 2.32108, 2.39845, 2.47582, 2.55319, 2.63056, 2.70793, 2.78530, 2.86267, 2.94004, 3.01741, 3.09477, 3.17214, 3.24951, 3.32688, 3.40425, 3.48162, 3.55899, 3.63636, 3.71373, 3.79110, 3.86847, 3.94584, 4.02321, 4.10058, 4.17795, 4.25531, 4.33268, 4.41005, 4.48742, 4.56479, 4.64216, 4.71953, 4.79690, 4.87427, 4.95164, 5.02901, 5.10638, 5.18375, 5.26112, 5.33849, 5.41586, 5.49322, 5.57059, 5.64796, 5.72533, 5.80270, 5.88007, 5.95744, 6.03481, 6.11218, 6.18955, 6.26692, 6.34429, 6.42166, 6.49903, 6.57640, 6.65377, 6.73113, 6.80850, 6.88587, 6.96324, 7.04061, 7.11798, 7.19535, 7.27272, 7.35009, 7.42746, 7.50483, 7.58220, 7.65957, 7.73694, 7.81431, 7.89167, 7.96904, 8.04641, 8.12378, 8.20115, 8.27852, 8.35589, 8.43326, 8.51063, 8.58800, 8.66537, 8.74274, 8.82011, 8.89748, 8.97485, 9.05222, 9.12958, 9.20695, 9.28432, 9.36169, 9.43906, 9.51643, 9.59380, 9.67117, 9.74854, 9.82591, 9.90328, 9.98065, 10.05802, 10.13539, 10.21276, 10.29013, 10.36749, 10.44486, 10.52223, 10.59960, 10.67697, 10.75434, 10.83171, 10.90908, 10.98645, 11.06382, 11.14119, 11.21856, 11.29593, 11.37330, 11.45067, 11.52803, 11.60540, 11.68277, 11.76014, 11.83751, 11.91488, 11.99225, 12.06962, 12.14699, 12.22436, 12.30173, 12.37910, 12.45647, 12.53384, 12.61121, 12.68858, 12.76594, 12.84331, 12.92068, 12.99805, 13.07542, 13.15279, 13.23016, 13.30753, 13.38490, 13.46227, 13.53964, 13.61701, 13.69438, 13.77175, 13.84912, 13.92649, 14.00385, 14.08122, 14.15859, 14.23596, 14.31333, 14.39070, 14.46807, 14.54544, 14.62281, 14.70018, 14.77755, 14.85492, 14.93229, 15.00966, 15.08703, 15.16439, 15.24176, 15.31913, 15.39650, 15.47387, 15.55124, 15.62861, 15.70598, 15.78335, 15.86072, 15.93809, 16.01546, 16.09283, 16.17020, 16.24757, 16.32494, 16.40230, 16.47967, 16.55704, 16.63441, 16.71178, 16.78915, 16.86652, 16.94389, 17.02126, 17.09863, 17.17600, 17.25337, 17.33074, 17.40811, 17.48548, 17.56285, 17.64021, 17.71758, 17.79495, 17.87232, 17.94969, 18.02706, 18.10443, 18.18180, 18.25917, 18.33654, 18.41391, 18.49128, 18.56865, 18.64602, 18.72339, 18.80075, 18.87812, 18.95549, 19.03286, 19.11023, 19.18760, 19.26497, 19.34234, 19.41971, 19.49708, 19.57445, 19.65182, 19.72919, 19.80656, 19.88393, 19.96130, 20.03866, 20.11603, 20.19340, 20.27077, 20.34814, 20.42551, 20.50288, 20.58025, 20.65762, 20.73499, 20.81236, 20.88973, 20.96710, 21.04447, 21.12184, 21.19921, 21.27657, 21.35394, 21.43131, 21.50868, 21.58605, 21.66342, 21.74079, 21.81816, 21.89553, 21.97290, 22.05027, 22.12764, 22.20501, 22.28238, 22.35975, 22.43711, 22.51448, 22.59185, 22.66922, 22.74659, 22.82396, 22.90133, 22.97870, 23.05607, 23.13344, 23.21081, 23.28818, 23.36555, 23.44292, 23.52029, 23.59766, 23.67502, 23.75239, 23.82976, 23.90713, 23.98450, 24.06187, 24.13924, 24.21661, 24.29398, 24.37135, 24.44872, 24.52609, 24.60346, 24.68083, 24.75820, 24.83557, 24.91293, 24.99030, 25.06767, 25.14504, 25.22241, 25.29978, 25.37715, 25.45452, 25.53189, 25.60926, 25.68663, 25.76400, 25.84137, 25.91874, 25.99611, 26.07347, 26.15084, 26.22821, 26.30558, 26.38295, 26.46032, 26.53769, 26.61506, 26.69243, 26.76980, 26.84717, 26.92454, 27.00191, 27.07928, 27.15665, 27.23402, 27.31138, 27.38875, 27.46612, 27.54349, 27.62086, 27.69823, 27.77560, 27.85297, 27.93034, 28.00771, 28.08508, 28.16245, 28.23982, 28.31719, 28.39456, 28.47193, 28.54929, 28.62666, 28.70403, 28.78140, 28.85877, 28.93614, 29.01351, 29.09088, 29.16825, 29.24562, 29.32299, 29.40036, 29.47773, 29.55510, 29.63247, 29.70983, 29.78720, 29.86457, 29.94194, 30.01931, 30.09668, 30.17405, 30.25142, 30.32879, 30.40616, 30.48353, 30.56090, 30.63827, 30.71564, 30.79301, 30.87038, 30.94774, 31.02511, 31.10248, 31.17985, 31.25722, 31.33459, 31.41196, 31.48933, 31.56670, 31.64407, 31.72144, 31.79881, 31.87618, 31.95355, 32.03092, 32.10829, 32.18565, 32.26302, 32.34039, 32.41776, 32.49513, 32.57250, 32.64987, 32.72724, 32.80461, 32.88198, 32.95935, 33.03672, 33.11409, 33.19146, 33.26883, 33.34619, 33.42356, 33.50093, 33.57830, 33.65567, 33.73304, 33.81041, 33.88778, 33.96515, 34.04252, 34.11989, 34.19726, 34.27463, 34.35200, 34.42937, 34.50674, 34.58410, 34.66147, 34.73884
												}
											}}) {
			String lens = (String) o[0];
			
			lens2angles.put(lens, (double[]) o[1]);
		}
	}
	
	@Override
	public void setName(String name) {
		this.name = name;
	}

	@Override
	public String getName() {
		return name;
	}
	
	public Short[] getPassEnergies() {
		return new Short[] { 1, 2, 5, 10, 20, 50, 100, 200 };
	}
	
	public double getEnergyWidthForPass(int pass) {
		return 16.7478/200*pass;
	}
	
	public double getEnergyStepForPass(int pass) {
		return 16.119/200*pass;
	}
	
	public double[] getAngleAxis(String lensTable, int startChannel, int length) {
		if (!lens2angles.containsKey(lensTable)) {
			throw new ArrayIndexOutOfBoundsException("unknown lens table "+lensTable);
		}
		double[] doubles = lens2angles.get(lensTable);
		double[] copyOfRange = Arrays.copyOfRange(doubles, startChannel, startChannel + length);
		return copyOfRange;
	}
	
	public double[] getAngleAxis(String lensTable, int startChannel, int slices, int size) {
		if (!lens2angles.containsKey(lensTable)) {
			throw new IllegalArgumentException("unknown lens table "+lensTable);
		}
		int chunksize=size/slices;
		int handledsize=slices*chunksize;
		double[] doubles = lens2angles.get(lensTable);
		double[] values = Arrays.copyOfRange(doubles, startChannel, startChannel+handledsize);
		double[] mean= new double[slices];
		for (int i=0; i<slices; i++) {
			double mychunksum=0;
			for (int j=0; j<chunksize; j++) {
				mychunksum+=values[j+i*chunksize];
			}
			mean[i]=mychunksum/chunksize;
		}
//		AbstractDataset angledatasets=new DoubleDataset(values, slices, chunksize);
//		double[] mean = new double[slices]; 
//		for (int i=0; i<slices; i++) {
//			AbstractDataset slice = angledatasets.getSlice(new int[] {0, i}, new int[] {chunksize-1, i+1}, null);
//			mean[i] = Double.parseDouble(slice.mean().toString());
//		}
		return mean;
	}
	public String[] getLensModes() {
		return lens2angles.keySet().toArray(new String[0]);
	}
}