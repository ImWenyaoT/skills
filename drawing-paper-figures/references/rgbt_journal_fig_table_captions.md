# RGB-T Tracking 期刊论文图表审计

本文档从 `references/rgbt/tracking/journals/` 下的本地 PDF 批量抽取 Figure/Table caption，用于快速观察 RGB-T tracking 期刊论文通常画哪些图、放哪些表。

说明：caption 保留论文原文英文，方便后续回到 PDF 核对；自动抽取结果可能包含换行、断词或少量正文误匹配，正式引用前需要人工复核。

PDF 总数：41

## Contents

- 论文图表数量总览表（紧随其后，41 行，每篇一行的图数/表数）。
- 逐篇 caption 明细：每篇一个 `## <年份 venue 论文名>` 小节，内含「图：」与「表：」两段原文 caption 列表。小节顺序与总览表一致，按年份 + venue 排序（2020 → 2026）。
- 用法：先在总览表定位目标论文与图/表规模，再跳到同名 `##` 小节读具体 caption。

| 论文 | 图数量 | 表数量 |
| --- | ---: | ---: |
| 2020 IF Object Fusion Tracking Based on Visible and Infrared Images A Comprehensive Review | 23 | 7 |
| 2023 EAAI RGB-T Image Analysis Technology and Application A Survey | 17 | 8 |
| 2024 CVM Multi-Modal Visual Tracking Review and Experimental Comparison | 2 | 7 |
| 2024 IF RGBT Tracking A Comprehensive Review | 17 | 15 |
| 2025 IF Lightweight Robust RGBT Object Tracker with Jitter Factor and Kalman Filter | 13 | 11 |
| 2025 IF Multi-Modal Adapter for RGBT Tracking | 12 | 10 |
| 2025 IVC BTMTrack Dual-Template Bridging and Temporal-Modal Candidate Elimination | 7 | 6 |
| 2025 KBS MCINet Multimodal Context-Aware Network for RGBT Tracking | 14 | 14 |
| 2025 KBS MKFTracker Multimodal Knowledge Embedding and Feature Interaction | 13 | 5 |
| 2025 KBS Two-Stage Unidirectional Fusion Network for RGBT Tracking | 13 | 8 |
| 2025 NN MGNet Cross-Modality Cross-Region Mutual Guidance for RGBT Tracking | 15 | 6 |
| 2025 Neurocomputing FETA Frequency-Space Enhanced and Temporal Adaptative RGBT Object Tracking | 7 | 6 |
| 2025 Neurocomputing Frequency-Aware Feature Enhancement and Unidirectional Mixed Attention | 13 | 7 |
| 2025 Neurocomputing MCIT Multi-Level Cross-Modal Interactive Transformer for RGBT Tracking | 6 | 6 |
| 2025 OLE SFNet Dual-Enhanced RGBT Tracker | 10 | 4 |
| 2025 PRL Temporal Aggregation for Real-Time RGBT Tracking via Fast Decision-Level Fusion | 4 | 7 |
| 2025 PR UniRTL Universal RGBT and Low-Light Benchmark for Object Tracking | 14 | 17 |
| 2025 TCSVT MambaVT Spatio-Temporal Contextual Modeling for RGBT Tracking | 4 | 4 |
| 2025 TIP AFter Attention-Based Fusion Router for RGBT Tracking | 7 | 4 |
| 2025 TIP MV-RGBT Modality Validity Benchmark and MoETrack | 6 | 4 |
| 2025 TIP Revisiting RGBT Tracking Benchmarks from Modality Validity | 13 | 6 |
| 2025 TITS SiamTFA Triple-Stream Feature Aggregation for RGBT Tracking | 9 | 6 |
| 2026 EAAI Progressive Feature Learning with Alternate Fusion for RGBT Tracking | 7 | 12 |
| 2026 ESWA CoReTrack Consensus-Residual Fusion for Reliability-Aware RGBT Tracking | 13 | 6 |
| 2026 ESWA HATrack Cross-Modal Fusion with Heterogeneous Adapter for RGBT Tracking | 11 | 8 |
| 2026 ESWA RAMR Role-Adaptive Modality Recalibration Network for RGBT Tracking | 12 | 9 |
| 2026 ESWA TIPTrack Time-Series Information Prompt Network for RGBT Tracking | 8 | 5 |
| 2026 Electronics CMCLTrack Reliability-Modulated Cross-Modal Adapter and Cross-Layer Mamba Fusion | 7 | 5 |
| 2026 IF Adversarial Perturbation for RGBT Tracking | 13 | 8 |
| 2026 IF Cross-Modal Guiding Attention for RGBT Tracking | 9 | 9 |
| 2026 IVC STIFormer Spatial-Temporal Interaction Transformer for RGBT Tracking | 7 | 4 |
| 2026 Neurocomputing CAMT Cross-Modal Adaptive Modulation for RGBT Tracking | 9 | 7 |
| 2026 PR CAST Curriculum Adaptation for One-Stream RGBT Tracking | 7 | 8 |
| 2026 PR Category Text-Guided RGBT Tracking | 10 | 4 |
| 2026 PR Mining Representative Tokens for RGBT Tracking | 11 | 7 |
| 2026 PR RGBT Tracking via Supervised Mutual Guiding | 9 | 5 |
| 2026 PR Temporal Multimodal Knowledge Distillation for Modality-Missing RGBT Tracking | 9 | 4 |
| 2026 RIE SiamCCA Collaborative Channel-Spatial Aggregation for RGBT Tracking | 13 | 3 |
| 2026 TIP Causality-Based Modality and Platform Invariant Representation for Dynamic RGBT Tracking | 16 | 14 |
| 2026 TMM Scale-Aware Attention and Multimodal Prompt Learning for RGBT Tracking | 11 | 9 |
| 2026 TMM Video-Level Cross-Modal Temporal Navigation for RGBT Tracking | 7 | 8 |

## 2020 IF Object Fusion Tracking Based on Visible and Infrared Images A Comprehensive Review

图：
- Fig. 1: Examples of complementary information from visible and infrared images [17,36].
- Fig. 2: Development timeline of RGB-infrared fusion tracking. in high quality journals or well-known conferences [22–30]. As a consequence, the well-known visual object tracking challenge (VOT) started a new RGB-infrared subchallenge in 20191, aiming to attract researchers to evaluate the performances on provided video sequences. Note that since the appearance of tracking based on visible and infrared images,
- Fig. 3: Section 2 gives some background information. In Section 3, RGBinfrared fusion tracking methods are discussed in detail, including key points in implementation and diﬀerent fusion levels. In Section 4, we summarize the development of RGB-infrared datasets. Section 5 introduces the evaluation metrics. Section 6 presents experimental results and gives an analysis on the performances. Sections 7 discusses the fu-
- Fig. 4: Categories of RGB-infrared fusion tracking methods.
- Fig. 5: Pixel-level RGB-infrared fusion tracking.
- Fig. 6: Feature-level RGB-infrared fusion tracking. extraction of visible and infrared images, and the eﬀective fusion of them.
- Fig. 7: Decision-level RGB-infrared fusion tracking.
- Fig. 8: The framework of the compressive time-space Kalman fusion tracking algorithm [89]. Solid and dotted lines denote input and feedback directions, respectively.
- Fig. 9: However, mean-shift is a local deterministic search strategy, so it is easy to be trapped into local minimal and diﬃcult to recover from tracking failure.
- Fig. 10: Illustrations of modality weights [25]. The blue and red curve indicate the weights of visible and infrared images, respectively. It can be seen that the weights of visible and infrared images are almost consistent with their reliabilities. Therefore, the method can still work even though one modality has occasional perturbation.
- Fig. 11: Examples of modality weights computed in [69]. The weight of each image is shown under the corresponding image. (a) In the top image, the target is more discriminative form its surroundings, thus having a larger weight. (b) In the bottom image, the target is more clear than the top image, thus having a larger weight. In each subfigure, the left column
- Fig. 12: A general framework of graph-based RGB-infrared tracking method [29]. (a) Input images. (b) Partitioned patches. (c) and (d) represents the illustration of local and global relationship, respectively, where the red circle is taken as an example, and the green circles have relations with the red one. (e) Illustration of graph construction, where 9 graph nodes are shown for clarity. wi denotes the weight of the i-th node, and aij represents the edge weight of the i-th node and the j-th node. (f) Illustration of RGB-infrared features and foreground patch weights. (g) Final feature representation.
- Fig. 13: Pipeline of Cross-Modal Ranking for Robust RGB-infrared Tracking [28]. (a) Cropped regions, where the red bounding box indicates the region of initial patches. (b) Patch initilization indicated by red color. (c) Optimized results from initial patches. (d) Ranking results with the soft cross-modality consistency. (e) RGB-T feature representation. (f) Structured SVM. (g) Tracking results.
- Fig. 14: General framework of feature-level deep learning-based RGB-infrared fusion tracking algorithms.
- Fig. 15: The architecture of the method proposed by Zhang et al. [76].
- Fig. 16: Pipeline of the method proposed by Li et al. [26]. (a) Input frames. (b) Target patch. (c) Generic network. (d) Feature map selection (e) Correlation filter. (f) Tracking results.
- Fig. 17: The flowchart of FANet [77]. map. Based on the final response map, the position and scale of the target can be derived. A modality weight computation method was proposed there based on the response map of each modality. The method can run at around 28 FPS. An improved version of this method, called DSiamMFT, was also proposed by the same group [140]. Besides, Lan
- Fig. 18: The weights were obtained according to the response maps in the detection phase. Specifically, the average peak-to-correlation-energy (APCE) [110] was employed to compute weights. The speed of SCCF was 50 FPS, which satisfied the real-time requirement. Zhai et al. [30] proposed an RGB-infrared tracking algorithm via cross-modal correlation filters, as illustrated in Fig. 19. In that work, correlation filter was em-
- Fig. 19: The fast RGB-infrared tracking via cross-modal correlation filter [30].
- Fig. 20: The hybrid framework consists of two modules [79]. 177
- Fig. 21: Video examples and corresponding attribute annotations in the GTOT dataset [25]. In each image pair, the left one is visible image while the right one is infrared image. Red box is the bounding box of the target in the first frame. The words under each image pair give the name and annotated attributes of that image sequence.
- Fig. 22: Examples of unregistered visible and infrared images. • There is still a lack of benchmark, by using which one can compare the performance with other RGB-infrared trackers. Li et al. [71] made an early eﬀort to handle this by building the RGBT234 dataset. They also tried to provide results of some trackers. However, they are still not enough, because the results of most
- Fig. 23: Training thermal infrared trackers with generated infrared images using GAN [21]. (a)Image-to-image translation component for generating a large labeled synthetic infrared tracking dataset. Blue dashed line represents the baseline RGB training model and

表：
- Table 1: Examples of recent published researches on RGB-infrared fusion tracking.
- Table 2: Attributes annotated in GTOT [25]. Attribute Description Attribute Description OCC Partial or full occlusion TC Thermal crossover LSV Large scale variation SO Small object
- Table 3: Attribute information of RGBT210 and RGBT234 dataset [27,71].
- Table 4: Comparison of RGB-infrared fusion tracking datasets. Name Videos Frames (In total) Attributes Ground truth Video type Resolution Year OTCBVS 6 17K No No RGB, T 320 × 240 2005 LITIV 9 6.3K No No RGB, T 320 × 240 2012
- Table 5: Precision rate (PR %), Success rate (SR %) and running speed (FPS) on the GTOT dataset. The best three results are shown in red, green and blue, respectively. Best viewed in color.
- Table 6: clearly shows that deep learning-based methods achieve the leading performance on RGBT234 by outperforming graph-based and sparse representation-based approaches with a very clear margin. In particular, the top four results are all produced by deep learning-based methods. This indicates that deep learning techniques can improve RGB-
- Table 7: Speed of some RGB-infrared fusion tracking algorithms. Name/Reference Framerate (FPS) CPU or GPU Category Zhai [30] 227 CPU CF-based SCCF [74] 50 CPU CF-based

## 2023 EAAI RGB-T Image Analysis Technology and Application A Survey

图：
- Fig. 1: Spectral range contrast of the thermal infrared and the visible light.
- Fig. 2: Object for different imaging contrasts under low-light conditions. Fig. 2(a) is a visible light imaging display, which is difficult to distinguish the target objects. Fig. 2(b) is a thermal infrared imaging display where the two rows are clearly visible.
- Fig. 3: The increasing number of publications in RGB-T image analysis technology and application from 2012 to July 2022. Source: Data from Google scholar advanced search: ‘‘RGB-T’’, ‘‘visible and thermal’’ and ‘‘visible and LWIR’’.
- Fig. 4: The schematic diagram of the main application fields of RGB-T image analysis. challenging images from different scenes. Therefore, this dataset can better verify the robustness of the RGB-T SOD methods. Recently, Song et al. (2022a) constructed a variable illumination RGBT dataset named VI-RGBT1500, which is collected under three different illumination conditions including sufficient illumination, uneven illumination and
- Fig. 5: The structure of this paper.
- Fig. 6: Semantic segmentation results (%) on Tokyo-Multi-Spectral dataset. RGB and thermal image pairs in the annotated dataset are connected to form 4 channel images to train and test the proposed network; 1105,112 and 109 images for training, validation and testing respectively. The RoadScene-seg dataset is manually annotated with eight categories of common objects in autonomous driving scenes (unlabeled,
- Fig. 7: Detection results on CVC-14 dataset. There are currently two types of improved test annotations: the original annotations (Hwang et al., 2015) and the test annotation proposed by Liu et al. (2016) (denoted as 16). In addition, because this dataset is taken from video continuous frame pictures, adjacent pictures do not different, so a certain degree of sampling. The KAIST training set has
- Fig. 8: Comparison of computation time and miss rate on the UTokyo dataset. reasonable and full dataset settings, respectively. MCFF (Cao et al., 2021b) is the best among the existing detectors, with a 20.61% MR under the reasonable setting and a 49.52% MR under all settings, it fuses color and heat flow according to light conditions. Conversely, the results of the ACF + T + THOG (Hwang et al., 2015) are the worst
- Fig. 9: Attribute-based PR/SR scores (%) on GTOT dataset.
- Fig. 10: Attribute-based PR/SR scores (%) on RGBT210 dataset.
- Fig. 11: Attribute-based PR/SR scores (%) on RGBT234 dataset. DJI Phantom 4 Pro Plus v2.0 and the IR camera is the FLIR Vue Pro R. Dataset is from a video of backgrounds, including rail tracks, roads and woods select frames with different content to build. At this time, the dataset contained 400 VL-IR-matched images. In addition, VL images were augmented with day, night, fog, and snow conditions using
- Fig. 12: Evolution of RGB-T image fusion methods. Recently, the latent low-rank representation (LatLRR) model has been gradually attracted attention in image fusion. Li and Wu (2018c) introduced a novel image fusion method based on LatLRR. Li et al.
- Fig. 13: Evolution of RGB-T salient object detection methods. for visible and infrared image fusion (DenseGAN). Yang et al. (2021g) proposed an effective infrared and visible image fusion method based on a texture conditional generative adversarial network (TC-GAN).
- Fig. 14: Evolution of RGB-T semantic segmentation methods. fusion (RFF) to make full use of the robustness of thermal images.
- Fig. 15: Evolution of RGB-T pedestrian detection methods. two concepts of encoding-end fusion and independent module fusion, therein CCAFFM aims to guide the feature fusion process by obtaining the channel spatial correlation between thermal and RGB features.
- Fig. 16: Evolution of RGB-T object tracking methods.
- Fig. 17: Evolution of RGB-T person re-identification methods. was raised by Liu et al. (2022g). Xiao et al. (2022) depended on novel Attribute-based Progressive Fusion Network (APFNet) to increase the fusion capacity with a small number of parameters while reducing the dependence on large-scale training data. An RGBT tracking framework based on the transformer was designed by Feng and Su (2022), which

表：
- Table 1: , we present the experimental results of Mr under reasonable and full dataset settings, respectively. ‘‘Reasonable’’ means that only pedestrians with no occlusion or partial occlusion greater than 55 or 50 pixels were considered in the evaluation, while ‘‘full dataset’’ represents the evaluation of the entire data, including small pedestrians and heavy
- Table 2: Quantitative comparison results of different RGB-T image fusion methods on TNO dataset.
- Table 3: Quantitative comparison results of different RGB-T SOD methods.
- Table 4: Quantitative comparison results of different methods on Tokyo-Multi-Spectral, PST900, and RoadScene-seg datasets.
- Table 5: , we present the experimental results of Mr under reasonable and full dataset settings, respectively. ‘‘Reasonable’’ means that only pedestrians with no occlusion or partial occlusion greater than 55 or 50 pixels were considered in the evaluation, while ‘‘full dataset’’ represents the evaluation of the entire data, including small pedestrians and heavy
- Table 6: that the deep learning-based methods achieve the best results in both PR and SR. In particular, the top two methods in both PR and SR are deep learning-based, which outperform the graph-and filter-based methods with distinct advantages. This strongly demonstrates that deep learning can significantly improve the performance of RGB-T tracking.
- Table 7: Quantitative comparison results of different RGB-T person re-identification datasets.
- Table 8: The research progress of RGB-D-T image analysis. Ref. Year Sensors Image Resolution of Cameras Annotation Application Visible Depth Thermal 4D thermal imaging system 2011 Kinect v1+ULRvision TC384 640 × 480 640 × 480 384 × 288 – Medical Diagnostics

## 2024 CVM Multi-Modal Visual Tracking Review and Experimental Comparison

图：
- Fig. 6: These trackers achieve obvious performance advantages although the speed is low. Zhang et al. [74] proposed an end-to-end real-time RGB-T tracking framework with balanced accuracy. They applied ResNet [112] as the feature extractor and fused RGB and thermal information at the feature
- Fig. 7: The attribute description is provided in the Electronic Supplementary Material (ESM).

表：
- Table 1: Summary of existing surveys in related fields Index Year Reference Area Description Publication 1 2010 [34] Multi-modal fusion This paper provides an overview on multi-modal data fusion.
- Table 2: Summary of multi-modal tracking datasets Name Seq. Num. Total frames Min. frames Max. frames Attr. Resolution Metrics Year RGB-D PTB 100 21.5k 40 0.90k 11 640 × 480 CPE, SR 2013 STC 36 18.4k 130 0.7k 10 640 × 480 SR, Acc., Fail. 2018
- Table 3: Experimental results on the PTB dataset. The top three results are in red, blue, and green fonts Algorithm Target type Target size Movement Occlusion Motion type Human Animal Rigid Large Small Slow Fast Yes No Passive Active OTR 77.3 68.3 81.3 76.5 77.3 81.2 75.3 71.3 84.7 85.1 73.9
- Table 4: Most of the trackers cannot meet realtime tracking requirements. Trackers based on the improved CF framework (OTR [7], DMKCF [50], CCF [83], WCO [53], and TACF [51]), are constrained by their own speed. Two real-time trackers (DSKCF
- Table 5: Experimental results on the GTOT and RGBT234 datasets Tracker GTOT (SR/PR) RGBT234 (SR/PR) Speed Device Platform Setting LRMWT 75.3/91.1 61.6/82.5 24.6 GPU PT GTX 1080Ti HMFT 74.9/91.2 56.8/78.8 30.2 GPU PT RTX Titan ADRNet 73.9/90.4 57.1/80.9 25.0 GPU PT RTX 2080Ti
- Table 6: Challenge results on VOT2019-RGBD dataset Tracker Modality F-score Precison Recall SiamDW-D RGB-D 0.681 0.677 0.685 ATCAIS RGB-D 0.676 0.643 0.712 LTDSE-D RGB-D 0.658 0.674 0.643
- Table 7: Challenge results on the VOT2019-RGBT dataset Tracker Modality EAO Acc. R.

## 2024 IF RGBT Tracking A Comprehensive Review

图：
- Fig. 1: Complementary benefits of RGB and thermal data. (a) Benefits of thermal sources against RGB ones. (b) Benefits of RGB sources against thermal ones.
- Fig. 2: The development of RGBT tracking method and evaluation platform.
- Fig. 3: Illustration of the structural outline of this article. 2. Related work This section discusses in detail the relevant work that contributes to the understanding and implementation of RGBT tracking, which is divided into four parts: RGB tracking, thermal infrared tracking, image fusion, and a review of existing review methods.
- Fig. 4: The pixel-level fusion framework of RGBT tracking [36]. outstanding fusion tracking methods have been developed for RGBT tracking, categorized based on three fusion levels: pixel-level fusion, feature-level fusion, and decision-level fusion. The section will provide detailed explanations of these three fusion levels in RGBT target tracking.
- Fig. 5: The feature-level fusion framework of RGBT tracking [36].
- Fig. 6: The decision-level fusion framework of RGBT tracking [36]. trackers for visible and thermal infrared modes, each conducting target tracking and generating independent decision results. Subsequently, these decision results are integrated into the final target state determination through a designed fusion module. Decision-level fusion emphasizes the integration of decision results from the visible and
- Fig. 7: Illustration of the optimized weights based on the modal reliabilities [44]. The blue and red curves indicate the weights of grayscale and thermal sources, respectively.
- Fig. 8: Illustration of the structural outline of CMR method [49]. (a) Cropped regions, where the red bounding box represents the region of initial patches. (b) Patch initialization indicated by red color. (c) Optimized results from initial patches. (d) Ranking results with the soft cross-modality consistency. (e) RGB-T feature representation. (f) Structured SVM. (g) Tracking results.
- Fig. 9: The fast RGBT tracking via cross-modal correlation filter [54]. operations, the alternating direction multiplier method to solve the optimization model, and a weighted fusion mechanism for calculating the final response graph in the detection and positioning stage, these methods effectively enhanced tracking accuracy and robustness.
- Fig. 10: Pipeline of MDNet-based RGBT trackers [60]. The architecture consists of two shared layers (RGB and thermal), concatenate layers, and K branches of domain-specific layers.
- Fig. 11: Pipeline of the published Siamese-based RGBT trackers [39]. For fusion at feature level, the multi-modal fusion locates between the feature extraction and similarity evaluation.
- Fig. 12: Pipeline of SiamCDA [78], a representing RGBT tracker based on Siamese network. The overall network consists of four main parts: Siamese network for unimodal feature extraction, CA-MF module for multi-modal feature fusion, SiameseRPNs for region proposal generation and DAS module for region proposal selection.
- Fig. 13: Pipeline of Transformer-based RGBT trackers, such as MACFT [84]. It is divided into three parts, which are used for modal-specific/shared feature extraction, information fusion between modalities, and bounding box regression.
- Fig. 14: Pipeline of Transformer-based RGBT trackers, such as TBSI [91]. RGB and TIR image patches are embedded as tokens and fed into Transformer blocks for joint feature extraction and intra-modal search-template matching.
- Fig. 15: Pipeline of other deep learning-based RGBT trackers, such as JMMAC [98]. This method jointly models motion and appearance cues via two main components, i.e., multimodal fusion and motion mining. Multimodal fusion aims to fuse the appearance information in two modalities and improves the tracking accuracy by the MFNet.
- Fig. 16: Example frame pairs in LasHeR [109].
- Fig. 17: Example frame pairs in VTUAV [101]. Scenes super class (sequence length) are shown on the top. Sequence-level attributes are shown at bottom, including camera movement (C), deformation (D), extreme illumination (E), partial occlusion (P), full occlusion (F), scale variation (S), thermal clustering (H), fast moving (M), out-of-view (O), and low resolution (L).

表：
- Table 1: Summary of existing review methods in RGBT tracking fields. Author Year Area Description Walia [37] 2016 Multi-modal multicue tracking A general review of both single-modal and multi-modal tracking methods.
- Table 2: The advantages and disadvantages of main RGBT tracking methods.
- Table 3: Statistics comparison of RGBT tracking datasets. Benchmark Sequences Resolution Min frames Max frames Average frames Total frames Object classes Challenging attributes Year GTOT 50 384 × 288 40 376 157 7.8K 9 7 2016 RGBT210 210 630 × 460 40 4140 498 104.7K 22 12 2017
- Table 4: List of the attributes annotated to GTOT. Attribute Attribute description OCC Occlusion the target is partially or fully occluded.
- Table 5: List of the attributes annotated to RGBT210 and RGBT234. Attribute Attribute description NO No Occlusion the target is not occluded.
- Table 6: List of the attributes annotated to LasHeR. Attribute Attribute description NO No Occlusion the target is not occluded.
- Table 7: Quantitative results of the existing tested RGBT trackers on GTOT and RGBT234 datasets. The ✘ means that the tracker has no results on the corresponding dataset.
- Table 8: Quantitative results of the existing tested RGBT trackers on GTOT and RGBT234 datasets. The ✘ means that the tracker has no results on the corresponding dataset.
- Table 9: Attribute-based precision rate and success rate on RGBT234 dataset of the competitive RGBT trackers.
- Table 10: Quantitative results of the RGBT trackers with their single-modal trackers on RGBT234 dataset.
- Table 11: Quantitative results of the existing tested RGBT trackers on RGBT210 dataset. The ✘ means that the tracker has no results on the corresponding dataset.
- Table 12: Quantitative results of the existing tested RGBT trackers on VOT-RGBTIR2019 dataset.
- Table 13: Quantitative results of the existing tested RGBT trackers on LasHeR dataset. The ✘ means that the tracker has no results on the corresponding dataset.
- Table 14: Quantitative results of the existing tested RGBT trackers on VTUAV-short dataset.
- Table 15: The Git links for RGBT datasets and published code methods. Datasets/Trackers Git link OSU-CT [105] OSU-CT

## 2025 IF Lightweight Robust RGBT Object Tracker with Jitter Factor and Kalman Filter

图：
- Fig. 1: Flowchart of the adaptive modal fusion strategy.
- Fig. 2: Visualization of JF’s calculation: (a) image frames; (b) residuals of two successive frames; (c) results of image opening operation on residuals with the corresponding JFs shown below.
- Fig. 3: Calculations of JF of four video sequences from RGBT234 dataset: (a) baginhand; (b) bikeman; (c) baby; (d) cycle5. S. Pan et al.
- Fig. 4: Analysis of the sensitivity of the proposed JF in scenarios with subtle camera motion: (a) video sequence womancross (#59-#65) from RGBT234 dataset; (b) corresponding JF values; (c) magnified images of #64 and #65 with a red reference line to more clearly visualize the subtle camera motion occurs at #65.
- Fig. 5: Flowchart of the proposed tracker.
- Fig. 6: Modality weights of video sequences from RGBT234 dataset: (a) afterrain; (b) toy3; (c) car 10; (d) walkingman. S. Pan et al.
- Fig. 7: Comparison results on camera motion problem: (a1)-(a3) results of ours on baginhand video sequence; (b1)-(b3) results of STRCF on baginhand video sequence; (a4)-(a6) results of ours on baby video sequence; (b4)-(b6) results of STRCF on baby video sequence.
- Fig. 8: Results of different object types in scenarios with camera motion from RGBT234 dataset: (a) elecbike; (b) single3; (c) child1; (d) dog11.
- Fig. 9: Comparison on maximum PR on RGBT234 dataset. Fig. 10. Comparison on maximum SR on RGBT234 dataset. S. Pan et al.
- Fig. 11: Comparison on maximum PR on GTOT dataset.
- Fig. 12: Comparison on maximum SR on GTOT dataset.
- Fig. 13: Results of different methods in scenarios with camera motion and long-term occlusions: (a) baby from RGBT234; (b) balancebike from RGBT234.
- Fig. 14: Failure cases of the proposed method: (a) twoelecbike1 from RGBT234; (b) car from RGBT234. S. Pan et al.

表：
- Table 1: Complexity Comparisons Among Representative Trackers. Tracker (Ref.) Camera Motion
- Table 2: Comparison of PR (%) of different trackers on different conditions of RGBT234 dataset.
- Table 3: Comparison of SR (%) of different trackers on different conditions of RGBT234 dataset.
- Table 4: , PR/SR of ours are 2.9 %/7.7 % and 2.3 %/3.9 % surpassing RT-MDNet+RGBT on RGBT234 and GTOT dataset, respectively.
- Table 5: Comparisons with advanced DL-based trackers. Red, green, and blue respectively denote the top three results.
- Table 6: that after the introduction of cross-modal fusion strategy, the PR/SR of STRCF on the two datasets is increased respectively by 5.0 %/3.9 % and 10.0 %/6.1 %, which indicates that the tracker with fused features outperforms trackers without modality fusion. This is because the proposed cross-modal fusion strategy can integrate the two modal­
- Table 7: Ablation study results of trackers with/without JF on RGBT234.
- Table 8: Experimental results of sequences with CM/HO/PO from RGBT234.
- Table 9: Impact of learning rate α on PR and SR (ω = 0.5 and β = 0.5) Red, green, and blue respectively denote the top three results.
- Table 10: Impact of threshold β on PR/SR of the proposed tracker (α = 0.03andω = 0.5).
- Table 11: Impact of learning rate ω on PR and SR (α = 0.03 and β = 0.5) Red, green, and blue respectively denote the top three results.

## 2025 IF Multi-Modal Adapter for RGBT Tracking

图：
- Fig. 1: A comparison of tracking approaches based on a backbone RGB tracker: (a) the RGB tracking. (b) the full-model fine-tuning approach for RGB-T tracking. (c) RGB-T tracking with the prompt fine-tuning paradigm applied to the thermal infrared branch.
- Fig. 2: An overview of the proposed MAT architecture. Visible images and thermal infrared images are converted into tokens through the embedding layer and then fed into Transformer, with the visible branch on the top and the TIR branch at the bottom. The multi-modal Adapter {𝐴𝑙 }𝑁 𝑙=1 , which is inserted into the RGB branch, learns how the multi-modal features interact at each layer 𝑙, where (N = 12). 𝐵 × 𝐿 × 𝐶 denotes the dimensions of features. Specifically, 𝐵, 𝐿, and 𝐶 respectively represent batch size, token
- Fig. 3: The overarching structure of MixAdapter features a channel reduction process. ‘‘LF’’ stands for low frequency extractor and ‘‘HF’’ represents high frequency extractor.
- Fig. 4: The performance with Different Numbers of the MixAdapter Blocks. The tracking performance of the number of MixAdapter modules evaluated on the LasHeR test set. (a) presents the success plot. (b) shows the precision plot. (c) is the normalized precision plot.
- Fig. 5: Different fusion strategies of high and low frequency decomposition. For convenience, the upsample and downsample layers have been omitted. And ‘Maxpool’, ‘DWconv’, and ‘Avgpool’ represent their own three branches.
- Fig. 6: The visualization of response maps for full fine-tuning, ViPT, and MAT models on the RGBT234 dataset. (a) RGB flows. The green, red and yellow boxes represent the full finely-tuned model of OSTrack-RGBT, ViPT and MAT-tiny. (b) Thermal infrared flows. (c) The response map of the fully fine-tuned model. (d) The response map of ViPT. (e) response map of MAT-tiny.
- Fig. 7: The visualization of feature maps after applying the learnable gating filter scheme in RGB, TIR, and RGBT modalities, respectively on the LasHeR benchmark from sequence 10runone. The feature map within the RGB branch follows the integration of the learnable gating filter scheme. (c) The feature map within the TIR branch, after the instantiation of the learnable gating filter scheme. (d) Feature maps within both RGB and TIR branches, with the left side representing the feature map of RGB modality and
- Fig. 8: Success and Precision Plots on the LasHeR test set. ‘FFTrack’ represents the full fine-tuning model of OSTrack-RGBT.
- Fig. 9: The visualization of the learnable gating filter designed for MAT. The tokens enclosed by the red box are template tokens, and the rest are search region tokens.
- Fig. 10: A subjective comparison of the respective trackers on the RGBT234 dataset. From top to bottom, we show the results on four video sequences, i.e., car41, carlight, carnotfar and caraftertree. The first two rows represent the RGB and thermal infrared images of the car41 sequence and the carnotfar sequence, while the last two rows depict the RGB and thermal infrared images of the carlight sequence and the caraftertree sequence.
- Fig. 11: A subjective comparison of examples of tracking failures on the dataset RGBT234, taken from baby, biketwo, bike, balancebike sequences (from top to bottom). For the first two rows from baby and biketwo sequences, the RGB imagery encompasses more information than the TIR modality. The bikesequence provides a wealth of relevant information.
- Fig. 12: The visualization of the attention maps from different attention layers for the MAT-base model on a sequence from LasHeR. The order of the attention map is left to right and top to bottom. The first two rows represent the attention maps for thermal infrared images, while the last two rows are for RGB images. The visualization of the feature maps is performed every two layers, comparing the visualization results between configurations with (right) and without adapter modules (left) within each group. It can be observed that in low-light conditions, the target information is more prominent in the thermal infrared modality, whereas the RGB modality has weaker information. As the number of layers deepens, the contours of the target information in the RGB modality become increasingly prominent in comparison with the thermal infrared data. In addition, within each set of images, the presence of adapter modules results in a clearer depiction of the target’s outline and texture information compared to configurations without the adapter modules.

表：
- Table 1: A Comparison of RGB tracking datasets and RGB-T datasets. ‘‘M’’ denotes million and ‘‘K’’ represents thousand.
- Table 2: A comparison of different types of models on the LasHeR test set.
- Table 3: A comparison of the components of MixAdapter on LasHeR test set and RGBT234 dataset. For each modality, MixAdapter comes with three branches, with each branch consisting of two modules. The symbol ‘‘←’’ signifies a reverse arrangement, while ‘‘→’’ indicates a sequential arrangement. (The Bold is the best).
- Table 4: A comparison of the learnable gating filter on the LasHeR test set. (The Bold is the best). The ‘✓✓’ indicates that every encoder layer uses different learnable gating filters.
- Table 5: Comparison between learnable gating filters of different modalities and comparison of thermal modality eliminating Encoder layers, based on the LasHeR test set for MAT-base. (The Bold is the
- Table 6: Comparison for different fusion strategies of high and low frequency decomposition, based on the LasHeR test set for MAT-base.
- Table 7: , we analyse the minimum and maximum graphics memory necessary for our method MAT and full fine tuning MAT. We find that fully fine-tuned models increase the pressure on memory, trainable parameters, and computational load, with a maximum batch size of 32 under extreme conditions. The initial settings for OSTrack are
- Table 8: Attribute-based Success/ Precision score on the LasHeR dataset.
- Table 9: A comparison with the state of the art methods on RGBT234 dateset. ‘FFTrack’ represents the full fine-tuning model of OSTrack-RGBT.
- Table 10: A comparison with the state of the art methods on the GTOT dateset.

## 2025 IVC BTMTrack Dual-Template Bridging and Temporal-Modal Candidate Elimination

图：
- Fig. 1: Comparison of our cross-modal fusion approach with previous methods. (a) VIPT, injects TIR modality information as prompt-based auxiliary input into the RGB modality network. (b) TBSI, uses template tokens as a bridge to mediate interactions between the search regions of the two modalities. (c) Our model, filters target-relevant search region tokens before performing dual-temporal template bridging. (d) Example of a Transformer block.
- Fig. 2: The overall framework of our method. It integrates static and dynamic templates with search regions from RGB and TIR patches. These patches are tokenized and processed by a ViT backbone for feature extraction. The proposed TMCE strategy filters tokens based on temporal and modal relevance to reduce background noise. The TDTB module enables interactions between dual-temporal templates and search regions of both modalities. Finally, fused RGB and TIR features are passed to the tracking head to predict the target’s location.
- Fig. 3: Illustration of the dual-temporal template fusion process and the six MHCA operations within the TDTB module. For clarity, common components such as LayerNorm (LN), MLP, and residual connections within each Transformer block are omitted.
- Fig. 4: Qualitative comparison of our method with other RGB-T trackers on four representative sequences from the LasHeR dataset.
- Fig. 5: Visualization of attention maps between dual-template tokens and search region tokens in the two modality branches of our backbone. (a) RGB search region. (b) RGB attention map. (c) TIR search region. (d) TIR attention map.
- Fig. 6: Visualization of sequence-level tracking results on the LasHeR test set, accompanied by attention maps from the final layer of the backbone network.
- Fig. 7: Failure cases in tracking. For each image group, the left side shows the dynamic template and the corresponding target heatmap, while the right side presents the actual frame with the predicted bounding box. The green-bordered boxes indicate normal tracking status, whereas the red-bordered boxes highlight failure cases. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.) trees; the second involves tracking under low-light conditions; the third features a fast-moving basketball; and the fourth presents a scene with strong lighting, making it difficult to localize a boy riding a bicycle.

表：
- Table 1: Comparison of our model with other state of the art methods on the LasHeR, RGBT234, and RGBT210 benchmarks. The top three results are highlighted in red, blue, and green, respectively.
- Table 2: Effectiveness comparison of the proposed BTMTrack components and the TBSI [11] module on the LasHeR dataset. Speed tests are conducted on a single RTX 2080Ti GPU. The best results are highlighted in bold.
- Table 3: Performance comparison between our method and other RGB-T trackers on the LasHeR dataset, evaluated on a single NVIDIA 2080Ti GPU.
- Table 4: Performance comparison of the proposed TMCE with other elimination strategies on the LasHeR dataset.
- Table 5: Ablation study on the insertion layers of the proposed TDTB module on the LasHeR dataset.
- Table 6: Attribute-based Precision/Success scores on the LasHeR dataset. Metrics are taken directly from published results.

## 2025 KBS MCINet Multimodal Context-Aware Network for RGBT Tracking

图：
- Fig. 1: MCINet comprises key components including visual encoders for extracting basic target features, memory encoders for modeling historical information, frequency-guided text-vision interaction modules, and parallel prediction heads with RGB, thermal, and fusion modality branches, collaboratively enhancing semantic expressiveness and tracking performance in target perception.
- Fig. 2: Coordinate-based local information extraction and global fusion from reference and memory frames to enhance target features.
- Fig. 3: MCINet employs a specially designed longand short-range attention mechanism to eﬀectively incorporate both local continuous and global non-continuous historical information relevant to the current frame, thereby enhancing temporal modeling capabilities.
- Fig. 4: Text descriptions jointly generated by BLIP2 and Nanodet, and subsequently optimized by ChatGLM3.
- Fig. 5: MCINet builds text-visual interaction with word-to-pixel attention and Gaussian-guided semantic enhancement. To address this issue, as illustrated in Fig. 5(a), we introduce a semantic attention mechanism that aligns visual and textual semantics by learning region-word correspondence. Specifically, we first project both the frequency-enhanced visual feature 𝑀𝑝𝑟𝑒 and linguistic feature 𝐿 into a unified semantic space: 𝑀′
- Fig. 6: Attribute-based performance of MCINet on RGBT210 compared with other RGBT trackers.
- Fig. 7: Visualization of PR and SR metrics for MCINet, TBSI, and TATrack across six challenging scenarios: AIV, FL, HO, PO, MB, and TC. MCINet under these attributes. As shown in Table 3, MCINet achieves the best PR/SR performance in attributes such as NO and FM, and shows strong competitiveness in HO, TC, MB, and CM. However, its performance on LR and BC is relatively weaker, consistent with the results on RGBT210 [50]-likely due to the considerable overlap in content and
- Fig. 8: Attribute-based performance of MCINet on GTOT dataset compared with other RGBT trackers.
- Fig. 9: Visualization of PR and SR metrics for MCINet, HIPTrack, TATrack and AQATrack across five challenging scenarios: DEF, FM, HO, MB, and SV.
- Fig. 10: Visualization of frequency response maps from diﬀerent frequency modules on representative tracking scenarios.
- Fig. 11: To visually demonstrate the superior performance of MCINet, we select six video sequences from LasHeR for tracking performance visualization and compare it with multiple outstanding trackers.
- Fig. 12: Visualization of MCINet performance on representative extreme scenarios from LasHeR.
- Fig. 13: Comparison of tracking performance (PR/SR) between MCINet and representative trackers under six extreme challenges from LasHeR: LI, FM, LR, TO, FL, and SA.
- Fig. 14: MCINet was compared with current leading RGBT trackers in terms of tracking performance and speed on RGBT234. The bubble area in the figure represents the weighted sum of FPS and PR.

表：
- Table 1: Comparison with 12 excellent RGBT trackers on RGBT210. The top three results are highlighted in bold, italic, and underline, respectively.
- Table 2: Comparison with 18 excellent RGBT trackers on the RGBT234. The top three results are highlighted in bold, italic, and underline, respectively.
- Table 3: Challenge-based PR/SR (%) analysis of MCINet and 6 excellent algorithms on RGBT234: The best two values are highlighted in bold and italic.
- Table 4: Comparison with 20 excellent RGBT trackers on LasHeR. The top three results are highlighted in bold, italic, and underline, respectively.
- Table 5: Challenge-based PR/SR(%) analysis of MCINet and 8 excellent algorithms on LasHeR. The best two values are emphasized by bold and underline.
- Table 6: Performance comparison of MCINet variants with diﬀerent textual cue encoders.
- Table 7: Performance comparison of diﬀerent TVII variants on LasHeR. Variants PR NPR SR Variant-A 64.5 60.5 50.3
- Table 8: Performance comparison of diﬀerent target-related description generators for MCINet on LasHeR.
- Table 9: Performance comparison of diﬀerent historical cue strategies for MCINet on LasHeR.
- Table 10: Performance comparison of diﬀerent historical modeling variants on RGBT234.
- Table 11: Performance comparison of diﬀerent frequency variants on LasHeR.
- Table 12: Performance comparison of diﬀerent prediction head variants of MCINet on LasHeR.
- Table 13: Comparison of MCINet and recent excellent RGB-D/E trackers on three cross-modal datasets: VOT-RGBD22, DepthTrack, and VisEvent.
- Table i: mprovement, with PR, NPR, and SR increasing by 1.3 %, 1.4 %, and 0.7 %, respectively, compared to the no-description setting. Further gains were observed when BLIP2 [30] was used (Variant-C), yielding an additional 1.3 %, 0.8 %, and 0.4 % improvement in PR, NPR, and SR, respectively, over the BLIP-based variant. Although the BLIP2-enhanced

## 2025 KBS MKFTracker Multimodal Knowledge Embedding and Feature Interaction

图：
- Fig. 1: Illustration of MKFTracker’s tracking effectiveness in video sequences with target scale variation. MKFTracker introduces textual cues in the target tracking process to assist the estimation of the target scale through the high-level semantic information inherent in the image–text pairs. As shown in the figure, because the first image frame is a frontal target image, the tracker trained based on the first target image will incorrectly estimate the target scale when the target turns sideways in subsequent video frames. In contrast, with the introduction of textual cues, the tracker is able to use the higher-level semantic information of the target to facilitate more accurate target predictions. It is worth noting that we have displayed the tracking prediction boxes in each example image and have appropriately magnified them for easier observation and comparison.
- Fig. 2: The overall framework of MKFTracker. Our MKFTracker consists mainly of a text encoder for VLP, a visual feature extractor containing MMI and a classifier. MKFTracker uses SAR to improve tracking performance. First, we use RoIAlign to capture candidate region samples from the image features extracted by the visual feature extractor and obtain preliminary target locations by feeding them to the classifier. Next, we extract label semantic information by using the VLP text encoder. Finally, SAR takes advantage of the inherent semantic information of image–text pairs and the unique advantages of image patterns to refine the tracking results.
- Fig. 3: Architecture of shallow CNN networks.
- Fig. 4: Flow chart of the modal multilevel interaction module, which consists of modal interaction attention and modal multilevel attention.
- Fig. 5: Flow chart of embedded space operations.
- Fig. 6: PR (%) and SR (%) metric comparisons between MKFTracker and ten excellent RGBT trackers are based on the five challenges of LSV, SO, LI, OCC, and FM in the GTOT dataset. The top three best results are magnified and highlighted in red, blue, and green.
- Fig. 7: A visual comparison of MKFTracker with four advanced trackers was performed in four video sequences of the GTOT dataset. MANet++, ADRNet, and DMCNet, across five distinct challenge categories: Large Scale Variation (LSV), Small Object (SO), Low Illumination (LI), Occlusion (OCC), and Fast Motion (FM). Our algorithm consistently leads across all five challenges in terms of Success Rate (SR) metrics and exhibits competitive performance against these ad-
- Fig. 8: Visual comparison of our tracker versus four state of the art trackers on six video sequences of the RGBT234 dataset.
- Fig. 9: Comparison of ablation experiments on RGBT234. shape, and both the variant without SAR and the baseline train their classifiers using only target image features, leading to some tracking drift. In contrast, the SAR component refines target box estimation by leveraging the semantics inherent in image–text pairs, improving the tracking success rate. Fig. 10 illustrates that while all three variants
- Fig. 10: Visual comparison of ablation experiments on RGBT234.
- Fig. 11: The SR (%) performance metrics of MKFTracker and three variants based on a subset of challenge fingers from the RGBT234 dataset are compared.
- Fig. 12: The PR (%) performance metrics of MKFTracker and three variants based on a subset of challenge fingers from the RGBT234 dataset are compared.
- Fig. 13: Accuracy–speed plot on RGBT234.

表：
- Table 1: Precision Rate (PR) and Success Rate (SR) scores (%) of our tracker on the GTOT, RGBT210, RGBT234, and LASHER test sets are compared with other MDNet-based trackers. The best and second-best results are highlighted in red and blue, respectively.
- Table 2: Precision Rate (PR) and Success Rate (SR) scores (%) of our trackers on the GTOT, RGBT210, RGBT234, and LASHER test sets are compared with those of advanced discriminative trackers and Siamese-based trackers. The best and second-best results are highlighted in red and blue, respectively.
- Table 3: Tracking results (PR/SR) under each attribute on the RGBT234 dataset. The best and second-best results are highlighted in red and blue, respectively.
- Table 4: Comparison of different parameters on RGBT234. U1 U2 PR (%) SR (%)
- Table 5: Comparison of different thresholds on RGBT234. T PR (%) SR (%) FPS

## 2025 KBS Two-Stage Unidirectional Fusion Network for RGBT Tracking

图：
- Fig. 1: Comparison between the existing prompt learning RGBT Tracking Paradigm and TUFNet. (a) Previous framework for asymmetric prompt fine-tuning [13,15]. (b) Previous framework for symmetric bidirectional adapter prompt fine-tuning [14]. (c) Our proposed TUFNet leverages upstream model knowledge to unidirectionally guide the extraction of auxiliary modality features, facilitating the fusion of the two modalities in the process.
- Fig. 2: The architecture of the proposed TUFNet, comprises two main components: (a) The encoder module of TUFNet extracts visual features from input RGB and TIR image pairs and establishes correspondences between template and search regions. The superscripts of the modules indicate the layer number. (b) The decoder module of TUFNet utilizes the extracted visual features to autoregressively predict the target’s coordinate sequence.
- Fig. 3: Prior to the multi-head attention, the first stage of TUF fusion takes place and involves two input branches: RGB and thermal infrared search and template joint feature tokens 𝐻𝑖 𝑟 and 𝐻𝑖 𝑡 , where 𝑖 indicates the layer level of the Transformer Encoder Block. The first stage fusion
- Fig. 4: Detailed transformer block in the autoregressive causal decoder. This block utilizes Masked Multi-head Self-Attention to ensure that each element in the coordinate sequence is dependent solely on preceding elements during prediction. Additionally, it integrates visual features into the decoder through multi-head attention layers.
- Fig. 5: Attribute-based success rates of TUFNet on the GTOT and RGBT210 dataset compared with other RGBT trackers.
- Fig. 6: Comparison of PR/SR curves for TUFNet and six open-source RGBT tracking methods on the RGBT234 dataset.
- Fig. 7: Comparison for the PR/NPR/SR curves of TUFNet with those of six other open-source RGBT tracking methods on the LasHeR dataset.
- Fig. 8: The LasHeR dataset is employed to conduct a qualitative comparison on four typical and challenging scenarios, which are sampled video sequences, using three Prompt fine-tune RGBT tracking methods.
- Fig. 9: Failure cases on darktreesboy and leftmirror sequences in the LasHeR dataset.
- Fig. 10: The comparison of PR (%) and SR (%) metrics between TUFNet and its variants is based on the six challenges (NO, HO, LI, TC, DEF, and BC) on the RGBT234 dataset.
- Fig. 11: Different variants of two-stage unidirectional fusion strategy for dual-stream encoder framework.
- Fig. 12: Visualization of attention maps.Here, ‘‘TUFNet’’ represents our method, ‘‘TUFNet-C’’ represents the bidirectional fusion variant of our method.
- Fig. 13: The tracking performance and speed of TUFNet and state of the art RGBT trackers were compared on the RGBT234 dataset. The bubble area represents the weighted sum of FPS and SR.

表：
- Table 1: The Comparison with 12 state of the art RGBT trackers on GTOT and RGBT210, the best top two data are highlighted in Red, Blue.
- Table 2: The Comparison with 17 state of the art RGBT trackers on RGBT234, the best top two data are highlighted in Red, Blue. Results are reported in percentage (%).
- Table 3: Challenge -based PR/SR(%) analysis of TUFNet and 9 state of the art algorithms on RGBT234. The Best First Two Values are Emphasized by Red and Blue[56].
- Table 4: The Comparison with 17 state of the art RGBT trackers on LasHeR, the best top two data are highlighted in Red and Blue. Results are reported in percentage (%).
- Table 5: Challenge -based PR/SR(%) analysis of TUFNet and 9 state of the art algorithms on LasHeR. The Best First Two Values are Emphasized by Red and Blue[58].
- Table 6: Comparison results of TUFNet and its variants on RGBT234 datasets. ✓means adding the corresponding component.
- Table 7: Quantitative comparison between different variants of twostage unidirectional fusion strategy on the RGBT234 dataset.
- Table 8: Comparison of parameters and performance of different fine-tuning methods. Results are reported in percentage (%).

## 2025 NN MGNet Cross-Modality Cross-Region Mutual Guidance for RGBT Tracking

图：
- Fig. 1: Comparison of speed (FPS) and accuracy (PR) for state of the art methods on the LasHeR dataset. The size of each circle represents the weighted sum of speed and accuracy, with larger circles indicating better overall performance.
- Fig. 2: The architecture of the proposed MGNet consists of twelve stacked Transformer blocks, with fusion occurring after each block. The CCDA module and the MIFF module, whose full names are detailed in the legend, play crucial roles in the tracking process. The CCDA module adopts a dual-stage attention strategy to generate mixed features, effectively achieving mutual guidance of cross modal and cross regional features. Meanwhile, the MIFF utilizes multi-scale fusion strategy to fuse the changed feature. Notably, the two MIFFs following each Transformer block share weights.
- Fig. 3: The previous method of processing features for fusion.
- Fig. 4: The first stage process in the Cross-modality and Cross-region Dual-stage Attention (CCDA) module focuses on mixing different modality features. In this process, we mix different regional features of different modalities to generate mixed features for mutual guidance.
- Fig. 5: The second stage process in the Cross-modality and Cross-region Dual-stage Attention (CCDA) module aims to emphasize distinct regions within different modalities while minimizing the loss of modal information. First, mixed attention is applied to focus on various regions across modalities. Next, two residual connections are established, using the feature information of the same modality as the template region. Finally, the feature information processed by the Adapter that has the same modality as the search region to perform element-wise add.
- Fig. 6: The architecture of the proposed Multi-scale Intra-region Feature Fusion (MIFF). First, two pooling operations are employed to fuse the spatial feature information of the region. Next, convolution kernels of different sizes capture the feature information of regions at different scales, where sizes are 1, 3, 5, and 7. Finally, element-wise multiplication is used to retain the original crucial information while enhancing the sensitivity of features to changes at different scales. This process enables the fusion of features from different modalities within the same region.
- Fig. 7: MPR and MSR curves of different tracking methods on RGBT234 dataset. from different modalities and regions. By integrating TIR and RGB template regions and search regions, MGNet achieves mutual guidance of cross modal features and captures richer cross modal representations.
- Fig. 8: PR and SR curves of different tracking methods on GTOT dataset. Quantitative Evaluation on LasHeR Dataset. The LasHeR dataset is particularly challenging for object tracking tasks due to its inclusion of numerous long and challenging videos. The proposed method is tested on the LasHeR test dataset and the test results with different trackers are summarized and plotted in Table 2. As shown in Table
- Fig. 9: PR, NPR and SR curves of different tracking methods on LasHeR dataset. Analyze the CCDA Module and MIFF at Different Layers Feature fusion across different layers is long a focal point in RGBT tracking research, with its influence on network performance warranting deeper investigation. To assess the effectiveness of the proposed CMD and MIFF fusion methods at various layers, we perform a series of ablation
- Fig. 10: PR and SR radar images of different tracking methods under different challenge attributes on LasHeR dataset.
- Fig. 11: Visualize without CCDA module or MIFF tracking results. Neural Networks 190 (2025) 107707 11
- Fig. 12: Visualize using CCDA module and MIFF at different layers tracking results. mixing strategy on tracking performance, we visualized two different mixing processes, with results shown in Fig. 13. Fig. 13 reveals that when both mixing strategies are applied together, the tracking network achieves high accuracy. In contrast, removing either the first or second mixing process leads to notable deviations in tracking results. This
- Fig. 13: Visualize with or without dual mixed strategy in CCDA tracking results. and lighting variations, making the target harder to distinguish. In cases (4) and (5), the target is unclear in both modalities, highlighting the necessity of combining information from both thermal and visible images to achieve accurate tracking.
- Fig. 14: Visualize the tracking results of different tracking methods in different scenarios. The different colors of the tracking box represent different tracking methods. Green represents Ground Truth, red represents Ours, blue represents APFNet, yellow represents Un-Track, and purple represents ViPT.
- Fig. 15: Visualize tracking failure cases under specific challenges, such as small targets, occlusions, and other issues.

表：
- Table 1: Comparison of key innovations of several prominent works. Method Key innovation APFNet (Xiao et al., 2022) Attribute-based progressive fusion
- Table 2: Comparison with different trackers on the GTOT, RGBT234, and LasHeR testing sets. The higher the score, the better the tracker performance. The two best results are highlighted in red and blue font (Cheng, Lu, Zhang, Li, & Wang, 2022; Hong et al., 2024; Hou, Ren, & Wu, 2022; Hou et al., 2024; Long Li, Lu, Hua Zheng, Tu, & Tang, 2019; Lu, Li, Yan, Tang, & Luo, 2021; Lu, Qian, Li, Tang, & Wang, 2022; Peng, Zhao, & Hu, 2022; Wang et al., 2022; Wu et al., 2024; Yang, Li, Zheng, Leonardis, & Song, 2022; Zhang, Guo, Jiao, Zhang, & Han, 2023; Zhang, Wang, Lu and Yang, 2021; Zhang, Zhang, Zhuo, & Zhang,
- Table 3: Specific comparison results of different trackers under different challenge attributes on the LasHeR dataset. The higher the score, the better the tracker performance on that attribute. The two best results are highlighted in red and blue font.
- Table 4: The ablation results of the impact of the CCDA and MIFF modules on GTOT, RGBT234 and LasHeR dataset.
- Table 5: The ablation results of the impact of CCDA and MIFF modules at different layers on GTOT, RGBT234 and LasHeR dataset.
- Table 6: The ablation results of the impact of different fusions in the CCDA module on GTOT, RGBT234 and LasHeR dataset.

## 2025 Neurocomputing FETA Frequency-Space Enhanced and Temporal Adaptative RGBT Object Tracking

图：
- Fig. 1: The overall framework of FETA. The search and template regions from both visible light and thermal infrared branches are first processed through the embedding layer to obtain input tokens. During embedding, the FSE module facilitates feature extraction and information interaction between the search and template regions. The tokens are then fed into ConvMAE to achieve dual-modal feature interaction and fusion. Finally, the regression head provides the tracking results, and the OSP module generates confidence scores to ensure reliable template updates.
- Fig. 2: The overall architecture of the Frequency-Space Enhancement (FSE) module. The template features and search features are first processed through the frequency attention (FA) with shared weights, then input into the spatial enhancement module (SEM) to enhance channel and spatial interactions. Finally, the processed features are combined with the original features via residual connections to obtain the attention features for the template and search.
- Fig. 3: The pre-training strategy for Cross-Modal ConvMAE. We apply a random masking with a masking rate of 75% to the original image. The decoder then reconstructs the masked image blocks that are invisible.
- Fig. 4: Overall architecture of the Online Score Prediction (OSP) module. The score tokens, search tokens, and template tokens are fed into two decoder layers to obtain the prediction scores, enabling reliable updates of the online template.
- Fig. 5: The evaluation curves of our model compared to other models on the RGBT234 dataset.
- Fig. 6: The visualization results of our tracker compared to four other advanced trackers across four video sequences. TBSI* denotes the version of TBSI with pre-trained weights trained on the ImageNet1K dataset, which is aligned to our method. Compared to other advanced trackers, our tracker demonstrates significant performance improvements across all three metrics. Specifically, compared to the second-best SDSTrack, our tracker achieves improvements of
- Fig. 7: The evaluation curves of our model compared to other models on the LasHeR dataset.

表：
- Table 1: Tracking results (PR/SR) for each attribute in the RGBT234 dataset. The top three performances are highlighted in red, green, and blue, respectively.
- Table 2: Tracking results (PR/SR) in the VTUAV dataset. The top three performances are highlighted in red, green, and blue, respectively.
- Table 3: PR/NPR/SR metrics (%) on the RGBT234 and LasHeR datasets. Trackers RGBT234 LasHeR PR SR PR NPR SR BaseLine 82.5 59.8 62.1 58.8 49.4
- Table 4: Ablation studies of our proposed FSE module on PR/NPR/SR metrics (%).
- Table 5: As illustrated in Table 5, CMCMAE consistently outperforms ViT across all evaluation metrics. On the LasHeR dataset, CMCMAE demonstrates performance gains of 3.3%, 3.5%, and 2.7% in PR, NPR, and SR, respectively. These results highlight the advantages of CMCMAE’s
- Table 6: Ablation studies of our proposed OSP module on PR/NPR/SR metrics (%).

## 2025 Neurocomputing Frequency-Aware Feature Enhancement and Unidirectional Mixed Attention

图：
- Fig. 1: Comparison of our feature processing approach with other previous approaches. (a) Use CNN-based feature extraction for RGB and TIR respectively, and then perform feature fusion. (b) Use ViT-based feature extraction for RGB and TIR respectively, and then perform feature fusion. (c) Ours: Enhance TIR and RGB features respectively, and then perform multistage ViT-based fusion.
- Fig. 2: The overall framework of the proposed tracker. Our backbone composes of twelve ViT layers. Meanwhile, we adjusted the operation process of RGB and TIR in ViT with shared weight. The proposed ERFE which can effectively enhance features are inserted into the first to ninth ViT layers. The proposed BMFF which is composed of CFEA can effectively extract and fuse information of different modalities are embedded into each ViT layer. Finally, we concatenate the features processed by the twelfth ViT layer and feed them into the prediction head to obtain the final results of tracking.
- Fig. 3: The overall structure of Early Region Feature Enhancement (ERFE) module. It consists of two main components: the Frequency-aware Self-region Feature Enhancement (FSFE) block and Cross-attention Cross-region Feature Enhancement (CCFE) block. FSFE can enhance intra-region feature representation, enhancing the information of the template region itself and the search region itself. CCFE can enhance inter-region feature representation, capturing the information exchange between template and search regions.
- Fig. 4: The structure of the Complementary Feature Extraction Attention (CFEA) module. The proposed CFEA consists of two main parts: the Unidirectional Mixed Attention (UMA) block, which highlights target features within the search region, and the Context Focused Attention (CFA) block, which further emphasizes target feature information in template and search region. CFEA which is the key component of BMFF can effectively promote BMFF to fuse the information of auxiliary modality into the primary modality.
- Fig. 5: We compare the MPR and MSR values of different trackers on RGBT234 dataset. GTOT dataset contains images or videos from different sensors that simulate diverse perceptual environments in the real world. Based on this dataset multi modal information fusion methods can be further explored.
- Fig. 6: We compare the PR and SR values of different trackers on GTOT dataset. more than 20 methods to evaluate our model in general, and our method outperformed all the methods in the table, proving its effectiveness. Additionally, our method is tested on a subset of different challenging attributes, as shown in Fig. 8. Our method has a significant advantage over the other methods on this subset of challenging
- Fig. 7: We compare the PR, NPR and SR values of different trackers on LasHeR dataset.
- Fig. 8: We compare the PR and SR scores of different trackers with challenging attributes on LasHeR dataset.
- Fig. 9: The evaluation curves of MSR for 17 challenging attributes on the LasHeR dataset. Neurocomputing 616 (2025) 128908 10
- Fig. 10: Visualize the tracking results after removing the stage 1 or stage 2 of the BMFF module. Green, red, blue, and yellow represent Ground truth, Ours, without stage 1, and without stage 2 respectively.
- Fig. 11: Visualize the tracking results of removing the block FSFE from ERFE, and removing the block UMA from CFEA. Green, red, blue, and yellow represent Ground truth, Ours, without FSFE, and without UMA respectively.
- Fig. 12: We compare the tracking results of different tracking methods in challenging scenarios and visualized them. The green, red, blue, yellow, and purple respectively represent the ground truth, our method, APFNet, Un-Track, and ViPT.
- Fig. 13: Visualize the failure cases of the proposed tracker. CRediT authorship contribution statement Jianming Zhang: Writing – review & editing, Supervision, Funding acquisition, Formal analysis, Conceptualization. Jing Yang: Writing – original draft, Software, Methodology, Formal analysis. Zikang Liu: Visualization, Data curation. Jin Wang: Validation, Investigation.

表：
- Table 1: Comparison with different trackers on the GTOT, RGBT234, and LasHeR testing sets. The higher the score, the better the tracker performance. The two best results are highlighted in red and blue font (see [37–46]).
- Table 2: The ablation results of precision and success rate for our proposed ERFE and BMFF modules.
- Table 3: The ablation results of ERFE module in different layers of the framework.
- Table 4: The ablation results of CFEA module in different stages of the framework.
- Table 5: In the Table 5, we find that when we remove the FSFE block and keep the CCFE our PR/SR drops by 2.2%/1.6% respectively, and also when we remove the CCFE block and keep the FSFE our PR/SR drops by 0.4%/0.2% respectively. Overall, the two key components FSFE and CCFE have a significant impact on the tracking results, thus
- Table 6: The ablation results of different components in CFEA. UMA CFA PR SR ✓ 68.0% 54.7% ✓ 68.1% 54.6%
- Table 7: The computational cost ablation results of our proposed ERFE and BMFF modules.

## 2025 Neurocomputing MCIT Multi-Level Cross-Modal Interactive Transformer for RGBT Tracking

图：
- Fig. 1: The overall network architecture of the MCIT. The MCIT extracts image features from RGB and TIR modalities through a shared ViT. The CMI modules are inserted behind the Transformer blocks at different layers for information interaction between two modalities. Finally the target position is predicted by the WAH.
- Fig. 2: The structure of the cross-modal interaction (CMI) module. where 𝐿𝑁(⋅) and 𝑀𝐿𝑃 (⋅) denote the layer normalization and multilayer perceptron, respectively. 𝑀𝑆𝐴(⋅) denotes the multi-head selfattention, which is computed as: 𝑀𝑆𝐴(𝑋) = 𝑠𝑜𝑓𝑡𝑚𝑎𝑥( (𝑋𝑊𝑄)(𝑋𝑊𝐾 )𝑇
- Fig. 3: Illustration of the window-based attention head (WAH). where 𝑀𝐶𝐴(⋅) denotes the multi-head self-attention, which is computed as: 𝑀𝐶𝐴(𝑋1, 𝑋2) = 𝑠𝑜𝑓𝑡𝑚𝑎𝑥( (𝑋1𝑊𝑄)(𝑋2𝑊𝐾 )𝑇 √
- Fig. 4: Comparison with advanced trackers on RGBT234 dataset.
- Fig. 5: Comparison with advanced trackers on RGBT210 dataset. Neurocomputing 649 (2025) 130758 7
- Fig. 6: Qualitative comparison of MCIT against seven state of the art trackers on three video sequences from LasHeR dataset. also involves inserting 4 layers of CMI. This is because they did not fully interact with the information of the last layer of the encoder.

表：
- Table 1: The PR (%) and SR (%) scores on the LasHer dataset against advanced trackers. The best, second best and third best results are in red, green and blue colors, respectively.
- Table 2: The PR (%) and SR (%) scores on the VTUAV dataset against advanced trackers.
- Table 3: Tracking speed and attribute-based PR/SR (%) scores on the RGBT234 dataset against seven RGBT trackers. The best, second-best and third-best results are red, green and blue colors, respectively.
- Table 4: The PR (%) and SR (%) scores on the LasHeR dataset for the different insertion layers of the CMI module.
- Table 5: From the experimental results, it can be observed that adding either of the two interaction modules can improve the performance of the model. Using CMI composed of two interaction modules simultaneously can achieve higher performance. This proves that the two interaction modules in CMI have a significant impact on performance
- Table 6: The PR (%) and SR (%) scores on the LasHeR dataset for the different heads.

## 2025 OLE SFNet Dual-Enhanced RGBT Tracker

图：
- Fig. 1: Overall architecture of the SFNet. fed into a sequence of transformer blocks. We embedded two key mod­ ules within the transformer blocks: Global-Local Modality Refinement (GLMR) and Frequency-Spatial Modality Fusion (FSCMF), which collab­ oratively perform feature extraction, feature enhancement, and cross­ modal interaction functions. Ultimately, the tracking head receives the
- Fig. 2: Overall architecture of the GLMR. features via a depthwise separable convolution and pointwise convolu­ tion: 𝐹local(𝑋) = 𝐵𝑁(𝐷𝑊 𝐶𝑜𝑛𝑣3×3(𝐵𝑁(𝐶𝑜𝑛𝑣1×1(𝑋)))) (5) where 𝐷𝑊 𝐶𝑜𝑛𝑣 denotes depthwise separable convolution and 𝐵𝑁 rep­ resents batch normalization. To enhance multi-scale feature aggrega­
- Fig. 3: Overall architecture of the FSCMF. and then transformed back to the spatial domain using the inverse FFT: 𝐴 = Re ( −1 (𝐴)
- Fig. 4: Frequency Analysis and Attention Distribution in the Proposed FSCMF Module. (a): Spectral decomposition of RGB and TIR template regions. FFT is applied to extract magnitude spectra and reconstruct lowand high-frequency components, revealing that RGB favors high-frequency structural cues while TIR retains low­ frequency thermal stability. (b): Frequency-domain attention maps from the two FSA branches (template and search regions). Vertical activation patterns indicate consistent attention to key frequencies, supporting the eﬀectiveness of FSCMF’s frequency-adaptive fusion.
- Fig. 5: PR and SR scores on LasHer dataset.
- Fig. 6: MPR and MSR scores on RGBT234 dataset. structed by masking out this central region, retains fine-grained edges and texture.
- Fig. 7: Comparison of SFNet With and Without the FSCMF Module. (a) Tracking results on RGB and TIR frames show that SFNet provides more accurate target localization compared to its variant without the FSCMF module.(b) Frequency analysis and response heatmaps of SFNet. The red box indicates the prediction and the green box denotes ground truth.
- Fig. 8: Visualization of heat maps of RGB feature, TIR feature and fusion feature of the search area on LasHeR [50] based on Grad-CAM. The Fusion Heat Map represents the heatmap of the sum feature of the RGB and TIR modalities. The fusion feature’s heat map is only displayed in RGB modality.
- Fig. 9: Qualitative comparison between our method and other RGB-T trackers on four representative sequences from LasHeR dataset.
- Fig. 10: Representative failure cases under challenging conditions. strategies to enhance the algorithm’s applicability in real-time applica­ tions.

表：
- Table 1: Comparison with state of the art trackers on RGBT210 [52], RGBT234 [51] and LasHeR [50]. Higher values indicate better performance. The best two results are shown in red and blue. (For interpretation of the colors in the table(s), the reader is referred to the web version of this article.) Method Source Backbone
- Table 2: Comparison of performance, model parameters, and computational complexity on the LasHeR dataset [50]. For performance metrics (PR, NPR, SR), higher is better. For model complexity (Params, FLOPs), lower is better. The best two results are shown in red and blue.
- Table 3: Ablation Studies of GLMR and FSCMF Modules in the Tracking Pipeline.
- Table 4: Ablation Studies of Diﬀerent Insert Layers of our GLMR and FSCMF Modules.

## 2025 PRL Temporal Aggregation for Real-Time RGBT Tracking via Fast Decision-Level Fusion

图：
- Fig. 1: The baseline method relies solely on spatial information (a), while TAAT fuses both spatial and temporal information (b). Notably, our method incorporates a fast fusion module at the decision level, ensuring real-time efficiency. In our DFM, adaptive fusion weights are learned in a TIR-assisted way, denoted as TIR->RGB.
- Fig. 2: Architecture of the original RPN Head (a) and our TIAM (b). where C denotes a single convolutional layer. 𝑟𝑔𝑏𝑐𝑙𝑠_𝑝 and 𝑡𝑖𝑟𝑐𝑙𝑠_𝑝 are the positive classification maps from RGB and TIR modalities. In Fig. 1(b), an attention map (Att) is initially learned from RGB data to suppress information from non-salient regions in the TIR modality. After traversing a convolutional block, the suppressed TIR features are further combined
- Fig. 3: Comparison between our TIAM and baseline tracker. discriminative features in both modalities, benefiting both temporal information aggregation and multi-model fusion procedures.
- Fig. 4: Analysis of failure cases. first row, unpredictable camera movements occur and the continuity is broken, leading to tracking failures. In the second row, long-lasting occlusion and extremely weak signal are two more challenging factors for drifted predictions. These factors are generally caused by the weakness of the feature extractor. Therefore, our future work will mainly

表：
- Table 1: Ablation studies on four benchmarks. Dataset VOT-RGBT2019 GTOT VTUAV LasHeR Metric EAO (↑) SR (↑) SR (↑) SR (↑) TIR 0.2439 0.6010 0.3670 0.2580
- Table 2: Quantitative results on VOT-RGBT2019 dataset. Method HMFT† [20] DMCNet [14] mfDiMP [24] ADRNet [25] JMMAC(A) [26] DFAT [7] ViPT† [5] MPT [31] CAFF [32] TAAT
- Table 3: Comparison on GTOT, RGBT210, and VTUAV datasets. Tracker GTOT RGBT210 VTUAV PR(↑) SR(↑) PR(↑) SR(↑) PR(↑) SR(↑) SiamFT 0.8220 0.7000 – – – –
- Table 4: Modality significance in DFM. Variant A (↑) R (↑) EAO (↑) RGB->TIR + TIR->RGB 0.6408 0.7062 0.4063 RGB->TIR 0.6475 0.7233 0.4058
- Table 5: Efficiency analysis for the proposed method on VTUAV. Component Backbone Neck fusion-DFAT fusion-JMMAC Times (s) 0.0061 0.0002 0.0003 0.0124 Component RPN TIAM DFM Total
- Table 6: Exploring the channels of our DFM on VOT-RGBT2019 dataset. Index Channel A (↑) R (↓) EAO (↑) FPS (↑) #1 1-16-8-1 0.6388 0.2915 0.3980 52 #2 1-32-16-1 0.6400 0.2833 0.4091 51
- Table 7: Efficiency analysis: fusion block & results on VOT-RGBT2019. Level Method Algorithm Time (s) EAO Pixel-level Addition DFAT(MDLatLRR-based) [7] 0.0001 0.3481 Feature-level Learnable ADRNet [25] 0.0015 0.3959

## 2025 PR UniRTL Universal RGBT and Low-Light Benchmark for Object Tracking

图：
- Fig. 1: Example frame triplet in UniRTL. Here we list examples of sequential images for different scenarios, time periods, object categories and tasks to demonstrate the diversity of UniRTL. The first row shows the thermal infrared images, the second row shows the low-light images, and the third row shows the visible images. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.)
- Fig. 2: Imaging platform for capturing video sequences of UniRTL benchmark. (a) Example of the captured frame triplet. (b) The optical axes of three cameras. (c) Result of the globally aligned data. (d) Images that have been cropped and precisely aligned.
- Fig. 3: Distribution of scene illuminance in UniRTL benchmark. The horizontal axis represents the illuminance of the scene. The vertical axis represents the number of image triplet. We divide the illumination of the scene into three levels: ‘‘𝑙𝑜𝑤-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’, ‘‘𝑚𝑖𝑑𝑑𝑙𝑒-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’, and ‘‘ℎ𝑖𝑔ℎ-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’. The number of attribute challenges in each level of the scene is shown in the blue box. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.)
- Fig. 4: Distribution of object categories in UniRTL benchmark. The horizontal axis represents category types. The left vertical axis (namely, the blue histogram) represents the number of video sequences, while the right vertical axis (namely, orange line graph) represents the average pixel size of the object category. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.)
- Fig. 5: The proposed baseline Unismot is comprised of three main components: (1) detector, (2) data associator, and (3) FTP. The detector includes three key elements: (1) unified inputs, (2) backbone with feature fusion module and (2) unified head.
- Fig. 6: Detector architecture. The network architecture adopts Darknet53 [17]. FTP means first-frame target prior. The FPN feature (P3, P4, P5) and the feature embedding generated by FTP are fed into the head.
- Fig. 7: Network structure of multimodal fusion strategies. low-score bounding boxes is generally neglected in the traditional associators, which only focus on efficiently utilizing high-scoring detection boxes. This paper introduces the strategy of reusing low-scoring detection boxes to maintain robust feature integration and stable tracking under challenging illumination conditions.
- Fig. 8: Re-ID long-term matching (RLM) module. The red arrow represents the dataflows of the query detections in the instance Box. The motion state of the template is updated and the tracking result is obtained when the query detection feature matched by the advance appearance similarity (AAS) module matches the template tracking feature. On the contrary, the tracking result is obtained purely according to the Kalman motion state of the template. Notably, the template tracking feature refers to the target
- Fig. 9: Advance appearance similarity (AAS) module. Motion distance includes the Mahalanobis and Euclidean distances. The red arrows represent the dataflows of query detection features. The black arrows represent the dataflows of the template tracking feature. When the two feature successfully match, the template tracking feature is updated to the query detection feature. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.)
- Fig. 10: Evaluation results on entire UniRTL SOT dataset using normalizes precision (NPR), precision (PR) and success rates (SR).
- Fig. 11: Evaluation results on UniRTL SOT test set using normalizes precision (NPR), precision (PR) and success rates (SR).
- Fig. 12: Comprehensive performance comparison of our proposed Unismot with other 12 SOT and MOT methods on UniRTL test set. The five metrics on the left side of the radar chart are for the MOT task, while the three on the right side are for the SOT.
- Fig. 13: Qualitative evaluation in three representative sequences: football_41019_1_47, minibus_41007_2_228, and person_41011_13_203. Each color of detection box represents a tracker. Every pair of rows corresponds to the same sequence. The images at upper row are in TIR modality, and the lower row is from RGB images. FID: frame ID. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.)
- Fig. 14: Visualization of the results in the sequence ‘person_41012_11_285’ with a similar appearance (SA) challenge. The bounding box delineates in red signifies the target required for tracking in the single object tracking (SOT) task. The yellow bounding boxes represent other objects with their own trackIDs that have a similar appearance. FID: frame ID. (For interpretation of the references to color in this figure legend, the reader is referred to the web version of this article.)

表：
- Table 1: Comparison of UniRTL benchmark against other tracking datasets. All results are directly obtained from the paper.
- Table 2: Details of the three cameras. FOV, field of view; EFL, effective focal length; SR, spectral range.
- Table 3: Description of two new challenges in the UniRTL benchmark. Attributes Description TD Thermal Drift Some thermal frames are lost or unstable.
- Table 4: The annotations data format of the UniRTL benchmark. Position Name Description 1 Frame ID Specify the frame in which the object appears.
- Table 5: Results of 6 different popular trackers on the UniRTL MOT test set.
- Table 6: Tracking performance of 10 SOT trackers on UniRTL SOT dataset in three illumination environments (‘‘𝑙𝑜𝑤-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’, ‘‘𝑚𝑖𝑑𝑑𝑙𝑒-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’ and ‘‘ℎ𝑖𝑔ℎ-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’). The evaluation metrics are NPR, PR and SR.
- Table 7: Tracking performance of 6 MOT trackers on UniRTL MOT dataset in three illumination environments (‘‘𝑙𝑜𝑤-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’, ‘‘𝑚𝑖𝑑𝑑𝑙𝑒-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’, and ‘‘ℎ𝑖𝑔ℎ-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’). The evaluation metrics are HOTA, DetA, and AssA.
- Table 8: Results of PR and SR scores based on 16 challenges for 10 trackers on the entire UniRTL SOT dataset. The final row in the table displays the speed metrics for these trackers. Notably, our method uses the Unismot_m model.
- Table 9: delineates performance results for MANet, APFNet, and our proposed algorithm across four RGBT tracking datasets. The retrained Unismot algorithm shows equivalent or superior efficacy on GTOT, RGBT234, and LasHeR test sets, highlighting its capability for a single task. Despite a moderate PR score (0.773) for the RGBT234 dataset,
- Table 10: delineates performance results for Unicorn, Bytetrack, and MOTRv2 across MOT17 and UniRTL MOT datasets. The results clearly indicates a heightened level of difficulty in conducting MOT on the UniRTL dataset as opposed to the MOT17 dataset. The results indicate that the performance on other datasets is significantly lower compared
- Table 11: Tracking performance of Tri-modal fusion (Fusion I) and Dual-modal fusion (Fusion II) on UniRTL test set.
- Table 12: Tracking performance of four fusion configurations on UniRTL benchmark in three illumination environments (‘‘𝑙𝑜𝑤-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’, ‘‘𝑚𝑖𝑑𝑑𝑙𝑒-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’ and ‘‘ℎ𝑖𝑔ℎ-𝑖𝑙𝑙𝑢𝑚𝑖𝑛𝑎𝑛𝑐𝑒’’). The evaluation metrics are NPR, SR, and HOTA.
- Table 13: Unismot_m achieves best performance in the SOT challenge, whereas Unismot_x has shown superior performance in the multipleobject tracking challenge. Unismot_x exhibits superior performance but at the cost of higher computational requirements, registering the highest scores in both Params and GFLOPs, indicating increased com-
- Table 14: Comparison of different association algorithms with UniRTL test set. KF means using Kalman filter. FTP means first-frame target prior. RLM means Re-ID long-term matching module.
- Table 15: Comparison of various similarity metrics employed in two associations of Unismot with UniRTL test set.
- Table 16: Comparison of different input in Advanced Appearance Similarity (AAS) module.
- Table 17: Comparison of different experiment with UniRTL test set. The model we choose is Unismot_l (TIR+RGB).

## 2025 TCSVT MambaVT Spatio-Temporal Contextual Modeling for RGBT Tracking

图：
- Fig. 1: Framework and efficiency comparisons of our proposed methods. (a) Unlike existing RGB-T tracking methods that usually take a single image pair as input and overlook temporal information, our framework uses vision Mamba to fully exploit the spatio-temporal contexts from the perspective of long-range appearance modeling and
- Fig. 2: Overall framework of our MambaVT. The video-level templates set and search region training samples are fed into patch embedding layer, and historical trajectory prompts are fed into coordinate embedding layer. The embedded vectors are all sent into bidirectional Mamba encoder for unified contextual modeling. Ultimately, the search region vectors are used for predicting object state and coordinate query vector is used for auxiliary supervision with ground-truth bounding box.
- Fig. 3: Various data input modes. (a) Concatenation variants of templates and search region vectors. (b) Different scan orientations of scan operator in SSM. “t”, “s” and “f” refer to template, search region and frame, respectively.
- Fig. 4: Qualitative comparison: before vs. after incorporating trajectory motion information ImageNet RGB Tracking Data PR↑ NPR↑ SR↑ ✗ ✗ 45.7 42.4 36.1 VideoMamba ✗ 59.9 56.0 47.1 Vim ✓ 68.4 64.7 53.9

表：
- Table 1: : Overall performance on four prevalent RGB-T evaluation benchmarks. Red/Green/Blue indicates the best/runnerup/third best results. Results are reported in percentage (%). The number in the subscript denotes the search region resolution.
- Table 2: : Ablation studies on the number of template images and trajectory prompts during training.
- Table 3: : Ablation studies on various data input modes. select the two challenging sequences and visualize the tracking results before and after incorporating motion information as illustrated in Fig. 4. In the first video, a person is running against a clustered background. It is obvious that rely-
- Table 4: : Ablation studies on different pre-training methods. serve that the VideoMamba (which has the same architecture as Vim) pre-training brings better tracking performance than the Vision Mamba (Vim) pre-training, indicating its greater feature representation. We believe that with the ongoing de-

## 2025 TIP AFter Attention-Based Fusion Router for RGBT Tracking

图：
- Fig. 1: Comparison of existing RGBT tracking models. (a), (b) and (c) indicate representation model, feature fusion model and decision fusion model.
- Fig. 2: Overall network architecture of AFter. Illustration of each fusion unit and router. ECA and SGE denote a channel attention [41] and a spatial attention [42] enhanced. The above operations can be formulated as follows: Atts = Sigmoid(γ(Fg · Fs) + β) FSE = Concat[Atts · Fs] s = 1, ..., C/G
- Fig. 3: Precision Rate (PR) and Success Rate (SR) of challenge attributes on the RGBT234 dataset.
- Fig. 4: Visualization of fusion structures in HAN under different scenarios. RGB TIR Baseline AFter RGB TIR Baseline AFter (c) pedestrian_123 (a) leftunderbasket (b) redmidboy (d) pedestrian_056
- Fig. 5: Comparison of feature maps between ToMPRGBT (third column) and HAN-based ToMPRGBT (fourth column).
- Fig. 6: Qualitative comparison of AFter against four state of the art trackers on six video sequences. collaborating modality information of different qualities. In Fig. 5 (c), both modalities suffer from the challenge of low resolution due to the small size of the pedestrians in the UAV view. However, the fixed structure of the baseline fusion strategy is poor to handle the effective fusion of the low
- Fig. 7: two instances of AFter tracking failure. V. CONCLUSION In this work, we present a novel attention-based fusion router (AFter) for RGBT tracking, which is the first investigation of dynamic multi-modal feature fusion in the field of RGBT tracking. We also design a hierarchical attention

表：
- Table I: , demonstrate the remarkable performance of AFter, thus confirming its effectiveness. Specifically, AFter achieves an impressive PR score of 84.9% and a commendable SR score of 72.5%. These scores indicate that AFter still exhibits high accuracy and robustness in RGBT tracking from the
- Table II: ABLATION STUDIES OF FUSION LAYERS AND ROUTERS IN HAN. Layers Router RGBT234 LasHeR HAN PR SR PR SR Params FLOPs
- Table III: ABLATION STUDIES OF FUSION UNITS IN HAN. N0 N1 N2 N3 RGBT234 LasHeR HAN PR SR PR SR Params FLOPs
- Table IV: ABLATION STUDIES OF HAN ON DIFFERENT FRAMEWORKS Method RGBT234 LasHeR PR SR PR NPR PR

## 2025 TIP MV-RGBT Modality Validity Benchmark and MoETrack

图：
- Fig. 1: (a) RGB tracking. (b) RGBT tracking. (c) The proposed benchmark inspired by the observed inconsistency between the data in existing benchmarks and the imaging conditions motivating RGBT tracking. (d) Taking into account the modality validity, a new problem when to fuse is posed in this work, which discusses strategies for multi-modality information fusion. ‘MMW’ is the abbreviation of ‘multi-modality warranting’. prgb, ptir, and prgbt represent the predictions produced by the RGB, TIR, and the fused (RGBT) experts, respectively.
- Fig. 2: (a) The statistics of the MV-RGBT benchmark and (b) a brief introduction of the key-point-based alignment. are collected in MMW scenarios. Additionally, based on the specific challenges unique to each modality, MV-RGBT is divided into RGB and TIR components. This division allows for a detailed analysis in a compositional manner, facilitating a more comprehensive assessment of the contribution of each
- Fig. 3: Pipeline of the proposed MoETrack. Considering three experts, RGB, TIR, and RGBT, a comparison of confidence scores is conducted to maintain the final prediction.
- Fig. 4: Visualisations on MV-RGBT. From top to bottom, the frames are sampled from ET Fish River3, ET Sign Wall1, ER Cat Lawn1, and ER Bottle Bedroom. Additionally, a straightforward comparison among the RGB, TIR, and RGBT experts is provided on the right side.
- Fig. 5: Qualitative analysis on MV-RGBT.
- Fig. 6: Analysis for proposed new problem when to fuse. the latter exhibits higher-quality data for the TIR modality.

表：
- Table I: A COMPARISON BETWEEN EXISTING RGBT TRACKING BENCHMARKS AND THE PROPOSED MV-RGBT BENCHMARK.
- Table II: and Figure 5 report the ablation study of combining multiple experts. Basically, consistent with other methods, the variant with only the fused branch is involved, dubbed as SETrack. Furthermore, in our method, the performance of each expert is also provided. The experts for RGB, TIR, RGBT
- Table III: QUALITATIVE ANALYSIS OF THE BENCHMARKS. PR/% GTOT RGBT234 LasHeR VTUAV-ST MV-RGBT MoETrack-RGBT 92.9 87.5 71.7 82.9 65.3 MoETrack-RGB 84.9 81.6 62.4 76.1 44.0
- Table IV: QUANTITATIVE RESULTS ON GTOT, RGBT234, LASHER, AND VTUAV-ST BENCHMARKS.

## 2025 TIP Revisiting RGBT Tracking Benchmarks from Modality Validity

图：
- Fig. 1: The proposed benchmark is inspired by the observed inconsistency between the data in existing benchmarks and the imaging conditions motivating RGBT tracking. ReRGB, ReTIR, and ReRGBT represent the reliabilities of predictions from RGB, TIR, and the fused (RGBT) experts, respectively. On the right side, the statistics on existing datasets are provided and the entire list is available at the project page.
- Fig. 2: (a) Object classes and scenes of the proposed MV-RGBT; (b) Illustration of the key point-based registration method.
- Fig. 3: Differences between the existing datasets and the proposed MV-RGBT. (a) and (b) shows the image-level differences through histogram. (c) depicts the differences of data distributions though T-SNE.
- Fig. 4: Pipeline of MoETrack. Based on ViT-B-256, MoETrack employs a mixture of experts. During training, the gradients of multiple experts are computed separately, resulting in a jointly optimised backbone. In the test stage, a modality switcher is utilised, only activating the modality with best-evaluated reliability.
- Fig. 5: Reasons for posing the new problem ‘when to fuse’ with samples from MV-RGBT (ET Person S katingRink and ER Bar Bedroom0).
- Fig. 6: Frame-level analysis for the new problem ‘when to fuse’ with samples from MV-RGBT (ET Virtual Game10 and ER Bar Bedroom1) and LasHeR (boyruninsnow).
- Fig. 7: Qualitative analysis on MV-RGBT and its subsets. of these bounding boxes, gi,c and pi,c. The subscript i means the index of the frame and c signifies ‘centre’. n is the total number of frames in the benchmark. ths and thp represent the thresholds for calculating the success rate sr and precision rate pr, respectively. In general, there are two metrics, IoU and the
- Fig. 8: Comparisons with 4 advanced methods on 10 challenging attributes on LasHeR.
- Fig. 9: Visualisations on MV-RGBT. From top to bottom, the frames are sampled from ET Fish River3, ET Sign Wall1, ER Cat Lawn1, and ER Bottle Bedroom.
- Fig. 10: Qualitative analysis of the proposed method with samples from ER Cat Lawn0 and ET Fish River0.
- Fig. 11: Specified comparisons on RGBand TIR-invalid videos.
- Fig. 12: Different fusion strategies at the decision level. (a) Averaging directly; (b) Online adaptive weighting; (c) Modality switch employed in our method; (d) Training strategy used in TFNet [69]; (e) Training strategy used in HMFT [10]; (f) Training strategy used in our method.
- Fig. 13: Modality selection and the predicted modality reliability. Fig. 13 illustrates samples from the same video sequence where both RGB and TIR data can be less informative, together with the predicted scores. In this way, the consistency between the change of dominating modality and scores certificates the precision of the predicted modality reliability.

表：
- Table I: A COMPARISON BETWEEN EXISTING RGBT TRACKING BENCHMARKS AND THE PROPOSED MV-RGBT BENCHMARK. ‘*’ REPRESENTS THE NUMBERS ARE RECALCULATED ON THE TEST SPLIT AND SUFFIX ‘ST’ MEANS SHORT-TERM
- Table II: QUALITATIVE ANALYSIS OF RGBT TRACKING BENCHMARKS rink, blocking the thermal radiation. To be comprehensive, averaged IoU scores are further computed (RGB:0.732 vs TIR:0.002), indicating that TIR modality falls in the dilemma
- Table III: QUANTITATIVE COMPARISONS WITH ADVANCED METHODS ON GTOT, RGBT234, AND LASHER. THE BEST AND SECOND RESULTS ARE HIGHLIGHTED WITH BOLD AND Italic Furthermore, methods based on different frameworks (MDNet [30], Siamese [6], DiMP [20], and Transformer [23])
- Table IV: ABLATION STUDIES ON GTOT, RGBT234, LASHER, VTUAV-ST, AND MV-RGBT
- Table V: ANALYSIS OF DIFFERENT FUSION STRATEGIES AT THE DECISION LEVEL the injection of meaningless or even harmful information from the invalid modality.
- Table VI: ANALYSIS OF GENERALISATION CAPACITY OF THE PROPOSED METHOD on this, choosing the results from the best-evaluated expert brings further improvement by providing response maps with less noise.

## 2025 TITS SiamTFA Triple-Stream Feature Aggregation for RGBT Tracking

图：
- Fig. 1: Comparison of our tracker with state of the art trackers in terms of precision and tracking speed on the RGBT234 dataset.
- Fig. 2: Visualization of joint-complementary attention weight maps in three scenarios. (a) The target is weakly discriminative in two modalities. (b) The target is disturbed by high illumination in the RGB modality. (c) The target is not discriminative in the TIR modality. The red boxes are the search regions and the green boxes are the target regions.
- Fig. 3: Typical multi-modal feature extraction and fusion network structures for RGBT tracking.
- Fig. 4: The overall network architecture of SiamTFA. Firstly, template images and search images for both modalities are fed into a shared backbone. The backbone is a triple-stream structure for extracting and fusing multi-modality features. Subsequently, the template and search features perform pixel-wise correlation to obtain a correlation map. Finally, the correlation map is fed into the header network to predict the location of the target. JCFA denotes the joint-complementary feature aggregation module.
- Fig. 5: The internal structure of the joint-complementary feature aggregation (JCFA) module. The JCFA module consists of three components: multi-modal channel attention (CA), multi-modal spatial attention (SA), and multi-stage CA. After completing multi-modal feature enhancement and aggregation in the first two components, the aggregated features are fused with the previous stage features in the multi-stage CA component.
- Fig. 6: Three attention structures for generating joint-complementary weights. (a) presents a naive structure for generating three attention weights. Based on this naive structure, (b) reduces redundant structures by utilizing shared convolutional blocks. (c) is our proposed depthwise shared attention structure, which replaces the ordinary convolutional layer with a depthwise convolutional layer.
- Fig. 7: The evaluation results on RGBT234 dataset compared with RGBT trackers.
- Fig. 8: The evaluation results on LasHeR dataset compared with RGBT trackers.
- Fig. 9: Qualitative comparison of SiamTFA against five state of the art trackers on four video sequences. (a) The target is partially occluded in the RGB modality. (b) The target is in a complex environment with similar objects and is accompanied by having large scale variations. (c) The target is interfered by high illumination in the RGB modality. (d) The target is heavily occluded in certain frames. For each sequence, the left image shows the frames of RGB modality and the right image shows the frames of TIR modality.

表：
- Table I: PR AND SR(%) SCORES ON THE RGBT210 DATASET AGAINST TEN RGBT TRACKERS. THE BEST, SECOND-BEST AND THIRD-BEST RESULTS ARE IN BOLD, UNDERLINE AND ITALICS, RESPECTIVELY CAT [43], TFNet [6], MDNet [8], C-COT [37]. The results
- Table III: The PR/SR scores of our proposed tracker reached Authorized licensed use limited to: HANGZHOU DIANZI UNIVERSITY. Downloaded on May 25,2026 at 14:59:27 UTC from IEEE Xplore. Restrictions apply.
- Table II: TRACKING SPEED AND ATTRIBUTE-BASED PR/SR(%) SCORES ON THE RGBT234 DATASET AGAINST SEVEN RGBT TRACKERS. THE BEST, SECONDBEST AND THIRD-BEST RESULTS ARE IN BOLD, UNDERLINE AND ITALICS, RESPECTIVELY
- Table IV: COMPARISON OF PR AND SR(%) SCORES ON THE RGBT234 DATASET FOR DIFFERENT BACKBONE NETWORK ARCHITECTURES. THE BEST RESULTS ARE IN BOLD modality features and enhances the RGB modality features
- Table V: COMPARISON OF PR/SR(%) SCORES FOR THE USE OF DIFFERENT ATTENTION MODULES.
- Table VI: COMPARISON OF PR/SR (%) SCORES ON THE RGBT234 DATASET, TRACKING SPEED, GFLOPS AND PARAMS FOR DIFFERENT ATTENTION STRUCTURES. THE GFLOPS AND PARAMS ARE MEASURED BY THE JCFA MODULE IN STAGE 4. THE BEST RESULTS ARE

## 2026 EAAI Progressive Feature Learning with Alternate Fusion for RGBT Tracking

图：
- Fig. 1: Overview architecture of the proposed method. The proposed tracking method consists of four main parts: a single-branch Transformer encoder backbone network, SFALF modules, CFD modules, and a bounding box head.
- Fig. 2: Structure diagram of the SFALF module. The proposed structure mainly consists of two units, including a learnable inter-modal weight adjustment unit and a modal joint unit. ⊗ denotes the element-wise product.
- Fig. 3: Structure diagram of the CFD module. The CFD module consists of parallel dual cross-attention blocks that perform cross-attention on the fused template, the fused search region and the modality-shared information.
- Fig. 4: Comprehensive comparison of tracking SR and speed on the LasHeR dataset. The circle diameter is in proportion to the size of model parameter.
- Fig. 5: Comparison with different numbers and locations of the CFD module. Number represents the numbers of the CFD module. Location represents the locations of the CFD module. Performance is evaluated on LasHeR in terms of SR score.
- Fig. 6: Visualization between our method and other RGB-T trackers on eight representative sequences which include multiple challenge attributes. Best viewed in color.
- Fig. 7: Tracking failed cases. objects, significant loss of bimodal information, and blurred targets, the model cannot accurately and quickly recapture the target, making it difficult to accurately identify the target location. These failed cases may be attributed to the fact that as a short-term tracker, we did not establish a time modeling mechanism, lacked an explicit re-detection

表：
- Table 1: The abbreviations used in this paper are in alphabetical orders.
- Table 2: Overall performance on LasHeR test set. We report Success Rate (SR), Precision Rate (PR), and Normalized Precision Rate (NPR). Best results are highlighted in bold. The suboptimal results are highlighted with an underline.
- Table 3: Overall performance on RGBT234 and RGBT210. We report Success Rate (SR) and Precision Rate (PR). Best results are highlighted in bold. The suboptimal results are highlighted with an underline.
- Table 4: Overall performance on GTOT and VTUAV. We report Success Rate (SR) and Precision Rate (PR). Best results are highlighted in bold. The suboptimal results are highlighted with an underline.
- Table 5: Modality-loss tests on RGB benchmarks. We report the AUC score on LaSOT dataset and the AO score on GOT-10k dataset.
- Table 6: Modality-loss tests on RGB-T benchmarks. We report Success Rate on LasHeR test set.
- Table 7: , compared with other strong trackers, our proposed model achieves strong performance under these challenging conditions. This outcome provides substantial evidence of its ability in fusing the complementary information between the two modalities, and demonstrates the model’s high robustness, even in complex scenarios such as target
- Table 8: Comparisons about the Params, FLOPs, and Speed. Performance is evaluated on LasHeR in terms of SR score.
- Table 9: Pipeline-level ablation of alternating progressive learning. Performance is evaluated on LasHeR.
- Table 10: Comparison between alternating and non-alternating structures. Performance is evaluated on LasHeR.
- Table 11: Comparison between the proposed structure and other candidate structures.
- Table 12: The influence of channel expansion ratio of LIMWA unit on performance.

## 2026 ESWA CoReTrack Consensus-Residual Fusion for Reliability-Aware RGBT Tracking

图：
- Fig. 1: Precision and speed comparison on LasHeR against state of the art trackers.
- Fig. 2: Overview of the proposed CoReTrack architecture. limits error propagation and yields a reliability cue to steer subsequent fusion.
- Fig. 3: Illustration of the proposed CRA. are less likely to leak into the shared core. As a result, the fused features stay cleaner and more stable across diﬀerent scenes and conditions.
- Fig. 4: Demonstration of our TRAD (Comprising TPG and RPAD) and RGM. symmetric KL divergence between the student streams. The final reliability prior 𝜌, which balances intrinsic confidence with mutual agreement, is formulated as: 𝜌 = 𝛽 (
- Fig. 5: The specific numerical values of our proposed method for each challenge are also presented in the figure. It can be observed that our CoReTrack demonstrates consistent robustness across varying conditions, maintaining distinct advantages in scenarios involving TC, SO, and DEF. This empirical success is attributed to two specific behaviors in the design of CoReTrack. First, regarding deformation and clutter,
- Fig. 6: Visualization results of PR, SR, and NPR on the LasHeR dataset. stable tracking but also localizes targets with consistently tighter bounding boxes than competing methods.
- Fig. 7: Visual comparison of our CoReTrack with five other trackers on the crouch, baketballwaliking, and scooter sequences from the RGBT234 dataset. illumination variation (e.g., LI), as well as modality-reliant failures (e.g., TC and SV), reflecting the stable behavior of CoReTrack across heterogeneous conditions.
- Fig. 8: Visual comparison of our CoReTrack with five other trackers on the boyunder2baskets, 1strowrightgirl3540, and carcomingfromlight sequences from the LasHeR dataset.
- Fig. 9: Correlation analysis between the normalized reliability prior 𝜌2 and the actual tracking IoU evaluated on the LasHeR test set.
- Fig. 10: Visual comparison of tracking results under diﬀerent temperature parameters 𝜏 on the bike and girl’sblkbag sequences.
- Fig. 11: Comparison of PR, NPR, and SR scores on the LasHeR dataset with diﬀerent temperature parameters 𝜏.
- Fig. 12: Visualization of tracking results with CRA and TRAD inserted at diﬀerent layers. The tracking bounding boxes are overlaid with heatmaps to highlight performance diﬀerences.
- Fig. 13: Eﬀectiveness of asymmetric supervision on the LasHeR dataset.

表：
- Table 1: Quantitative comparison with state of the art trackers on four benchmarks. The best and second-best results are highlighted in underline and bold, respectively.
- Table 2: Attribute-based comparison with state of the art trackers on RGBT234 dataset. underline, bold, and italic fonts indicate the best, second-best, and third-best results, respectively.
- Table 3: Attribute-based comparison with state of the art trackers on the LasHeR dataset in terms of Precision Rate (PR) and Success Rate (SR). underline, bold, and italic fonts denote the top three results.
- Table 4: Ablation study on the integration depth of the coupled CRA and TRAD.
- Table 5: Analysis of the eﬀectiveness of each component on the LasHeR and RGBT234 datasets.
- Table 6: Ablation study isolating the benefit of the proposed CRA module against standard feature concatenation.

## 2026 ESWA HATrack Cross-Modal Fusion with Heterogeneous Adapter for RGBT Tracking

图：
- Fig. 1: Spatial misalignment between infrared and visible images. The red box denotes the ground truth in the thermal infrared modality, while the green box represents the ground truth in the visible modality.
- Fig. 2: Overview of the HATrack framework. It comprises four components: a ViT backbone, a cross-modal spatial recalibration module (CFSR), a heterogeneous adapter module (HA), and a prediction head.
- Fig. 3: Cross-modal fusion spatial recalibration (CFSR) module. HL Block (High-low frequency block) ; SR Block (Spatial recalibration block). overall shape and layout of the target, while high-frequency information emphasizes edges and details. Enhancing low frequencies stabilizes the target’s shape and position, whereas high-frequency enhancement refines edge accuracy. This approach is especially eﬀective in infrared images, where it sharpens target contours and details, thereby reducing
- Fig. 4: High-low frequency module (HFR: High frequency refine; LFP: Low frequency projection; HFP: High frequency projection; GAP: Global average pooling; low_w: low frequency weights).
- Fig. 5: Gated residual adapter.
- Fig. 6: Bidirectional adaptive adapter module. 2 × 10−4 and is reduced by a factor of 10 after the 45th epoch. We adopt AdamW (Loshchilov & Hutter, 2017) as the optimizer. The template and search regions are resized to 128 × 128 and 256 × 256, respectively.
- Fig. 8: Comparison of PR/SR curves between HATrack and seven open-source tracking methods on the RGBT234 dataset (Li et al., 2019).
- Fig. 9: Comparison of HATrack with seven other tracking methods on the LasHeR test set (Li et al., 2021) in terms of PR, NPR, and SR curves.
- Fig. 10: Qualitative comparison of HATrack with three other methods across four classic scenarios in the LasHeR test set (Li et al., 2021). hancing target localization and significantly reducing the risk of tracking errors.
- Fig. 11: Visualization results of attention maps. HATrack Before and HATrack After represent the attention visualization eﬀects on the target before and after embedding the cross-modal fusion space recalibration module and the heterogeneous adapter module, respectively.
- Fig. 12: HATrack failure cases in extreme environments. were integrated and evaluated on the RGBT234 dataset (Li et al., 2019).

表：
- Table 1: Comparison of HATrack with ten other tracking methods on the GTOT dataset (Li et al., 2016). The best two results are highlighted in underline and bold. Results are reported in percentage (%).
- Table 2: Comparison of diﬀerent methods on the RGBT210 dataset (Li et al., 2017). The best two results are highlighted in underline and bold.
- Table 3: , HATrack ranks first among partially fine-tuned methods across PR, SR, and NPR, achieving a 3.3% SR gain over OneTracker (Hong et al., 2024) and surpassing fully fine-tuned SFNet (Zhang et al., 2025a) by 0.5% in SR, demonstrating its robustness in complex scenarios. Evaluation curves across PR, NPR, and SR in Fig. 9 further confirm the su-
- Table 6: Ablation of the internal components of the Cross-modal fusion spatial recalibration (CFSR) and heterogeneous adapter (HA) modules on the RGBT234 dataset (Li et al., 2019).
- Table 7: Comparison of HATrack with four representative trackers under RGB, TIR, and RGBT settings on the RGBT234 dataset (Li et al., 2019).
- Table 8: Analysis of computational complexity and runtime eﬃciency for diﬀerent modules.
- Table 9: Comparison of model complexity and inference eﬃciency between HATrack and four existing methods on the LasHeR dataset (Yang et al., 2023a).
- Table 10: Performance comparison after inserting the CFSR and HA modules into diﬀerent backbone tracking methods on the RGBT234 dataset.

## 2026 ESWA RAMR Role-Adaptive Modality Recalibration Network for RGBT Tracking

图：
- Fig. 1: Comparison of RAMR with existing RGBT tracking frameworks: (a) Asymmetric framework; (b) Symmetric framework; (c) RAMR integrates both advantages with modality quality assessment and adaptation.
- Fig. 2: Overview of the RAMR architecture: the left-side encoder extracts and enhances features from RGB and TIR images based on modality quality; the right-side pre-assessment network evaluates modality quality to determine the primary and auxiliary roles.
- Fig. 3: Architectural overview of the Quality-Aware Modality Switching module: a twin-stream framework evaluates RGB and TIR modalities via keypoint matching for shallow feature extraction and convolutional networks for deep semantic representation.
- Fig. 4: Combined illustration of RAMR’s modality processing modules. Left (AMFM): adaptive feature enhancement and role-aware fusion. Right (BCOM): semantic alignment and bidirectional vision-language refinement.
- Fig. 5: Failure tracking examples of RAMR in Low Resolution (LR) and Background Clutter (BC) scenarios.
- Fig. 6: Failure tracking examples of RAMR in Out-of-View (OV) and Abrupt Illumination Variation (AIV) scenarios.
- Fig. 7: Qualitative comparison on four representative and challenging scenarios from the LasHeR dataset. From top to bottom, the sequences are labeled as (a), (b), (c), and (d). The comparison includes three state of the art RGBT tracking methods and the proposed RAMR.
- Fig. 8: Visualization of RAMR’s generalization ability under extreme conditions.
- Fig. 9: Visualization of diﬀerent model variants to demonstrate the eﬀectiveness of QAMM and BCOM across various challenging scenarios, along with representative strategies for visualizing the attention mechanism in BCOM to further validate its performance.
- Fig. 10: PR and SR comparison of RAMR and five RGBT trackers under six challenging attributes on RGBT234.
- Fig. 11: Precision and Success Rate (with 95 % confidence intervals) of RAMR and representative trackers on LasHeR.
- Fig. 12: Comparison of RAMR and leading RGBT trackers on RGBT234 in terms of precision and speed. The bubble area represents the weighted sum of FPS and PR, indicating the trade-oﬀ between accuracy and real-time performance.

表：
- Table 1: Performance comparison of 10 competing methods on the GTOT and RGBT210 datasets. Best and second-best results are highlighted in bold and italic, respectively.
- Table 2: Performance comparison on RGBT234 with publication info. Best scores are in bold, second-best in italic, third-best in bold-italic.
- Table 3: Challenge-based PR/SR (%) analysis of RAMR and 9 outstanding algorithms on RGBT234: Best two values highlighted in bold and italic.
- Table 4: Performance comparison of our method with 18 outstanding RGBT Trackers.
- Table 5: Challenge-based PR/SR (%) analysis of 8 outstanding algorithms and our method on various Datasets, with best two values highlighted in bold and italic. Results are reported in percentage (%).
- Table 6: Comparison results of RAMR and its variants on RGBT234 and LasHeR. ✓ indicates the presence of the corresponding component.
- Table 7: Performance of QAMM layer configurations on RGBT234 and LasHeR (RAMR-v4 with QAMM and AMFM).
- Table 8: Performance comparison of diﬀerent modality confidence metrics used in QAMM on LasHeR.
- Table 9: List of key symbols and their meanings in the proposed RAMR. Symbol Description 𝑋𝑟, 𝑋𝑡 RGB and TIR search images

## 2026 ESWA TIPTrack Time-Series Information Prompt Network for RGBT Tracking

图：
- Fig. 1: The architecture of TIPTrack. TIPTrack is composed by two parts (feature encoding & fusion and sequential feature processing). Feature encoding & fusion extracts primary features of visible and thermal inputs, and then fuses RGBT features for sequential feature processing. Sequential feature processing predicts the bounding box of object according to learn time-series prompts and pass prompts for the next frames.
- Fig. 2: The preprocess of visible and thermal inputs. Visible and thermal inputs including templates and searching regions are cropped from original visible and thermal images by rounding the central point of object. Then, the inputs are divided into smaller patches that are further flattened to fit the input shape of ViT backbone.
- Fig. 3: Demonstration of DFB. generator (SPG) is designed to generate decisive feature. This decisive feature provide object information for searching head to locate object position, but also is reserved as the input feature of the sequential clue matcher (SCM) in next frame. SCM leverages the reserved feature of prior frame to identify variational features arised by object operation
- Fig. 4: Contracture of HiLoFF. HiLoFF consists of three parts that are high-frequency filter encoder (HFFE), low-frequency filter encoder (LFFE), and channel squeezer. HFFE and LFFE are designed to extract high-frequency and low-frequency features for visible and thermal images, respectively.
- Fig. 5: The archtecture of HiLoFF. Expert Systems With Applications 296 (2026) 129155 6
- Fig. 6: The working process of time-series prompt. Sequential prompt generator receives and processes input feature to generate prompt token. The prompt token is passed to sequential clue matcher where input feature is optimized by referencing to variational feature of the prompt token.
- Fig. 7: Visualized tracking result of partial sequences on RGBT234. There are six sub-figures that cover similarity interference, illumination variation, heavy occlusion, and low illumination.
- Fig. 8: Eﬀective analysis of RGBT234.

表：
- Table 1: Evaluated results of GTOT, RGBT210, RGBT234, and LasHeR. Pub.Info Year Method GTOT RGBT210 RGBT234 LasHeR PR SR PR SR PR SR PR SR
- Table 2: Evaluated results on short-term (ST) and long-term (LT) data of VTUAV.
- Table 3: The PR value of evaluated methods on 12 attributes of RGBT234. The red and blue fonts denote the first and second indexes of corresponding attributes, respectively.
- Table 4: The SR value of evaluated methods on 12 attributes of RGBT234. The red and blue fonts denote the first and second indexes of corresponding attributes, respectively.
- Table 5: Results of ablation methods on GTOT. DFBs Pos PR↓(%) SR↓(%) G1 A1 0 – 2.2 0.9

## 2026 Electronics CMCLTrack Reliability-Modulated Cross-Modal Adapter and Cross-Layer Mamba Fusion

图：
- Fig. 1: Overall architecture of the proposed CMCLTrack. Given a template–search pair in both RGB and thermal modalities, we first transform each modality input into token sequences via patch embedding and add positional encoding. The tokens are then processed by an N-layer dualstream Transformer backbone, where our Reliability-Modulated Cross-Modal Adapter (RMCA) is inserted to enable explicit bidirectional interaction between modalities. To further exploit hierarchical representations, we collect fused features from multiple backbone layers and aggregate them using the
- Fig. 2: The detailed architecture of RMCA. The top branch estimates modality reliability weights α, where N denotes the number of tokens in each modality. The bottom branch is a bi-directional adapter that down-projects tokens to D ′ and up-projects them back to D to produce cross-modal feature prompts.
- Fig. 3: Evaluation curves on LasHeR dataset. The representative scores of PR/SR are presented in the legend.
- Fig. 4: Attribute-based evaluation on the LasHeR dataset. https://doi.org/10.3390/electronics15050989
- Fig. 5: Training and validation loss variation during the trainings on the LasHeR dataset.
- Fig. 6: Visualization results on the LasHeR dataset. Figure 7 illustrates the visualization results on the VTUAV dataset. Compared with ground-based tracking scenarios, UAVs typically suffer from large viewpoint changes, rapid scale variations, and cluttered backgrounds. Under such challenging aerial perspectives, CMCLTrack is able to produce bounding boxes that are noticeably closer to the groundtruth target compared with other competing methods. This advantage mainly stems from
- Fig. 7: Visualization results on the VTUAV dataset. 5. Discussion Beyond benchmark evaluation, our reliability-aware RGB-T tracking framework may benefit a range of real-world monitoring applications, such as industrial inspection, intelligent surveillance, and construction safety. In construction sites, safety monitoring systems often operate with heterogeneous camera sources (e.g., fixed surveillance cameras

表：
- Table 1: Comparison of RGB-T tracking performance on GTOT, RGBT210, RGBT234, and LasHeR datasets. The arrows (↑) indicate that higher values are better. Bold numbers denote the best results in each column.
- Table 2: Performance on the VTUAV benchmark. The arrows (↑) indicate that higher values are better. Bold numbers denote the best results in each column.
- Table 3: Ablation study of key components on the LasHeR and VTUAV-ST dataset. The arrows (↑) indicate that higher values are better. Bold numbers denote the best results in each column.
- Table 4: analyzes the impact of different cross-layer fusion depths on tracking performance. Using only the last layer for fusion yields limited improvements, indicating that relying solely on high-level semantic features is insufficient for robust RGB-T tracking.
- Table 5: Performance and complexity comparison between Mamba-based and Transformer-based cross-layer fusion using encoder layers {4, 7, 10, 12}. Additional Params/FLOPs report the overhead introduced by the fusion module.

## 2026 IF Adversarial Perturbation for RGBT Tracking

图：
- Fig. 1: (a) Original cross-modal video frames without adversarial perturbations. (b)–(d) The attack performance comparisons on a SOTA RGB-T tracker BAT. Our perturbations can achieve a strong attack capability with high stealthiness on RGB-T tracker, which is tailored for the RGB-T tracking.
- Fig. 2: Overall framework of the proposed ICAttack. where {𝑎𝑒Φ𝑙 𝑣𝑖, 𝑎𝑒Φ𝑙 𝑖𝑟} indicate the adversarial cue features modulated and discovered by the visible and infrared modal characteristics, respectively. It is worth emphasizing that Φ𝑙
- Fig. 3: Structural diagram of the proposed intra-modal adversarial clues excavation (ImAE) and cross-modal adversarial collusion (CmAC).
- Fig. 4: Architectures of the spatial adversarial intensity control module (SICM). Finally, we maintain the original attack strength in the important regions while reducing the attack strength in non-important regions by a decay rate 𝜏, thus enhancing the stealthiness of the adversarial perturbations in a spatial dimension. Specifically, features Φ𝐿 𝑚 and Φ𝐿
- Fig. 5: Qualitative results on the RGBT234 dataset of four typical trackers(ViPT, TBSI, BAT, SDSTrack). Please zoom in for a better view.
- Fig. 6: Qualitative comparison results with the RGB-T tracker patch-based attack methods on the VTUAV dataset. Please zoom in for a better view.
- Fig. 7: Qualitative results on the LasHeR and GTOT datasets of four typical trackers (ViPT, TBSI, BAT, SDSTrack). Please zoom in for a better view. challenge scenarios to present the attack performance of our ICAttack, respectively.
- Fig. 8: Quantitative comparison of tracking performance on the LasHeR and GTOT datasets. The tracking performance of ViPT, TBSI, BAT, and SDSTrack trackers is reported, including the original performance without attacks and the performance under attacks. Lower tracking metrics PR and SR represent a better attack. Please zoom in for a better view.
- Fig. 9: Illustration of the eﬀectiveness of generated perturbations. The green, blue, and red boxes represent the ground truth, original results, and adversarial results, respectively. The blue and red lines represent the IoU’s variation of the original results and adversarial results over time, respectively. Better viewed in color with zoom-in.
- Fig. 10: Visual comparison of adversarial perturbations. Please zoom in for a better view.
- Fig. 11: Precision and Success Rates in diﬀerent attributes on RGBT234 and attack results on low-light tracking dataset NOT. Please zoom in for a better view.
- Fig. 12: The attack performance on the low-light degradation tracking RGB-T dataset NOT. Please zoom in for a better view.
- Fig. 13: Examples of the developed executable interactive interface.

表：
- Table 1: Comparison of attack performances on RGBT234 datasets. The best results are highlighted in light red and the suboptimal results are highlighted in light purple.
- Table 2: Comparison of attack performances with patch-based attack methods on VTUAV datasets. The best results are highlighted in light red and the suboptimal results are highlighted in light purple.
- Table 3: The generalized experiment of the unseen trackers during training.
- Table 4: The quantitative comparison results of the concealment of adversarial samples in visible, infrared, and after all perturbations are applied.
- Table 5: Quantitative comparison of ablation studies. Ablation 𝑝𝑟𝑜𝑗𝑡𝑒𝑥 𝑚𝑜𝑑𝑐𝑜𝑛 𝐼𝑚𝐴𝐸 𝐶𝑚𝐴𝐶 𝑆𝐼𝐶𝑀 Noise Branch PR SR SSIM Exp.1 ✗ ✔ ✔ ✔ ✔ ✔ 0.812 0.610 0.897 Exp.2 ✔ ✗ ✔ ✔ ✔ ✔ 0.660 0.478 0.938
- Table 6: Comparison experiment of diﬀerent feature fusion architectures.
- Table 7: Sensitivity of hyper-parameters in loss functions. Index 𝜆1 𝜆2 𝜆3 PR SR SSIM I 1.0 1.0 1.0 × 101
- Table 8: Sensitivity analysis on the hyper-parameters of radius 𝑟 in precise response disruption loss and threshold 𝜉 in token exchange and negotiation process.

## 2026 IF Cross-Modal Guiding Attention for RGBT Tracking

图：
- Fig. 1: Visualization of attention weights in the search region corresponding to the central part of the template. In (𝑎), search regions are shown for both modalities. For the two modalities, the attention weights are visualized as follows: (𝑏) demonstrates separate modeling using self-attention, (𝑐) showcases joint modeling using self-attention, and (𝑑) illustrates collaborative modeling using CGA block.
- Fig. 2: Comparison of performance and speed for SOTA tracking methods on LasHeR [18]. We visualize the PR against FPS. Closer to the top indicates higher performance, and closer to the right indicates faster speed. CGATrack ranks 1st in PR while running at 88.8 FPS.
- Fig. 3: The overall framework of our CGATrack. Our backbone network adopts the ViT with shared weights, while some MHA blocks are replaced with our proposed CGA block. The RGB and TIR search region features generated by the backbone network are combined and directly input into the tracking head to estimate the current target state.
- Fig. 4: The detailed architecture of the proposed BiWGM and BiFGM in CGA block. feature learning and consistency in multi-modal target relational modeling. It eﬀectively suppresses noise from erroneous and ambiguous correlation vectors during cross-modal interactions, thereby enabling bidirectional discriminative feature propagation and enhancement.
- Fig. 5: Various attention mechanisms. The diﬀerent colored lines indicate the diﬀerent features originating from 𝑸, 𝑲, and 𝑽 matrices.
- Fig. 6: Attribute-based evaluation on the RGBT234 dataset. The values in parentheses indicate the minimum SR on the left and the maximum SR on the right.
- Fig. 7: Visualization of the impact of the proposed CGATrack. (a) Target template. (b) Search region. (c) Separate modeling. (d) CGATrack.
- Fig. 8: Visualization of the cosine similarity between the search region features and the target template’s central position features.
- Fig. 9: Qualitative comparison of our method against four SOTA trackers on six video sequences.

表：
- Table 1: The abbreviations used in this paper are in alphabetical orders as follows: Nomenclature Referred to Nomenclature Referred to BC Background Clutter MB Motion Blur BiFGM Bidirectional Feature Guiding Module MHA Multi-Head Attention
- Table 2: The commonly used evaluation metrics in RGBT tracking. Metric Formula Explain Assessment Unit PR 𝑃𝑅 = 1 𝑁
- Table 3: The datasets used to evaluate our algorithm. Dateset Number Average Total Resolution
- Table 4: For a fair comparison, we initialize our model with pre-trained weights similar to those in [6,7,11,14], which are pre-trained on RGB tracking datasets such as COCO [47], LaSOT [48], GOT-10k [49], and TrackingNet [45].
- Table 5: Ablation studies of our proposed CGATrack. Values are presented as percentages (%).
- Table 6: Apply layers of the proposed CGA block on the LasHeR and RGBT234 datasets. Values are presented as percentages (%).
- Table 7: The scaling factor of the proposed BiWGM on the LasHeR dataset. Values are presented as percentages (%).
- Table 8: Quantitative comparison between diﬀerent variants of CGA block on the LasHeR dataset. Values are presented as percentages (%).
- Table 9: The variation trend of low-quality token proportion and IoU scores. Values are presented as percentages (%).

## 2026 IVC STIFormer Spatial-Temporal Interaction Transformer for RGBT Tracking

图：
- Fig. 1: Comparison of RGB-T tracking frameworks. (a) Mainstream RGB-T tracking framework with template update strategies. (b) Our framework with token propagation. The diﬀerence between the two frameworks is highlighted in green.
- Fig. 2: The framework of STIFormer, which includes spatial-temporal feature representation, token-guided mixed attention fusion, and prediction head.
- Fig. 3: The detailed design of the token-guided mixed attention fusion module. Linear Linear Linear Scaled Dot-Product Attention Concat Linear
- Fig. 4: Left:Multi-head Self Attention; Right:Scaled DotProduct Attention The detailed design of the token-guided mixed attention fusion module is illustrated in Fig. 3. The single-modality features are generated by their respective encoders. The modality features include frame features and token features,
- Fig. 5: Visualization results of (a)run1 sequence, (b)blancebike and (c)womanfaraway sequence, compared with MTNet [13], ViPT [48], HMFT [57] and DMCNet [19].
- Fig. 6: The visualization of search area features: the top row shows the feature visualization before applying the Tokenguided Mixed Attention Fusion, the middle row displays the features after the fusion, and the bottom row shows the original image, with the red box indicating the current search area and green box indicating the target.
- Fig. 7: Robustness analysis results of the proposed method compared with MTNet [13], ViPT [48], HMFT [57] and DMCNet [19].

表：
- Table 1: Comparison between the proposed method and the state-ofthe-art trackers on RGB-T datasets. The best results are highlighted in bold and the trackers that use temporal information are marked in *. The performance is evaluated in terms of
- Table 2: Comparison results of our method against the state of the art trackers. Attribute-based and overall performance are evaluated by PR/SR scores(%) and are produced on RGBT234 with DMCNet [19], MIRNet [20], HMFT [57], CAT++ [22], MTNet [13] and ViPT [48]. The best results are highlighted in Bold.
- Table 3: Multi-modal analysis on the RGBT234 Dataset, The best results are highlighted in Bold.
- Table 4: Ablation study of mixed attention fusion module on the RGBT234 Dataset, 𝑅 represents RGB and 𝑇 represents thermal modality. The best results are highlighted in Bold.

## 2026 Neurocomputing CAMT Cross-Modal Adaptive Modulation for RGBT Tracking

图：
- Fig. 1: Comparison of framework between previous works and our CAMTrack. (a) The symmetric framework employs a feature fusion module after feature extraction. (b) The asymmetric framework designating RGB as the dominant modality and TIR as the auxiliary modality. (c) The symmetric framework with simultaneous feature extraction and fusion in our method.
- Fig. 2: Overall framework of channel-adaptive modulation for RGB-T tracking. First, the two pairs of input images from both modalities are each concatenated and projected to generate embeddings, which are then fed into the backbone network for feature extraction. In the last three layers of the backbone network, we incorporate CAM modules to adaptively modulate the feature information of the two modalities. Finally, the features of both modalities are concatenated and fed into the tracking head to produce the final result.
- Fig. 3: The proposed channel-adaptive modulation module is illustrated by taking RGB as the dominant modality. First, tokens of the two modalities are concatenated along the channel dimension to obtain the input dimension. After global average pooling, the token sequence is dimensionally reduced to R1×2𝐷 , followed by weight adjustment using a linear layer. Finally, the result is passed
- Fig. 4: Our method achieves a comprehensive lead in SR over all compared advanced algorithms on GTOT, while its PR is only marginally lower by 0.9% than the state of the art method, CAT++.
- Fig. 5: The radar chart of tracking success rates for challenging attributes in the RGBT210 dataset shows th at CAMT leads significantly in challenging scenarios such as camera movement (CM), low illumination (LI), and heavy occlusion (HO), and scene complexity (SC), while achieving performance on par with stateof-the-art trackers in low resolution (LR) and no occlusion (NO) scenarios.
- Fig. 6: The MSR curve graph of the RGBT234 dataset based on challenging attributes shows that CAMT performs excellently in scenarios such as heavy occlusion (HO), low illumination (LI), and background clutter (BC), and also exhibits strong robustness in dealing with situations like camera movement (CM) and background clutter (BC).
- Fig. 7: Visualization of tracking results comparison between CAMT and five other state of the art trackers under challenging scenarios of the LasHeR dataset. Fig. 9 shows our CMTE module: after the third token elimina­ tion, the network has removed most irrelevant patches, drastically accelerating subsequent computations. By suppressing irrelevant noise, the model can focus better on the target region, improv­ ing performance to some extent. To quantify the contribution
- Fig. 8: The comparative diagrams of our CAM module are shown in the figure, where the first and second rows present before-and-after comparison diagrams under three different scenarios after applying CAM. The left side of each diagram corresponds to the RGB modality, and the right side corresponds to the TIR modality. The third row displays the ground truth of the target (green box) and the tracking results of our tracker (blue box).
- Fig. 9: Effect of the Proposed CMTE Module The figure demonstrates the token elimination results of different modalities in two scenarios. The shaded areas represent discarded parts, the blue boxes denote the ground truth, and the green boxes indicate the tracking results of our tracker.

表：
- Table 1: Comparison with state of the art trackers. The top 3 trackers are marked in red, and blue, respectively.
- Table 2: Performance of the LasHeR dataset based on challenge attributes. The top 3 trackers are marked in red, and blue.
- Table 3: Analysis of the impact of different components on performance, the best results are marked in red.
- Table 4: , the model achieves the best performance when the CAM module is embedded in the last three layers of the backbone. We attribute this to the fact that features extracted by early model layers are less refined and contain more noise, which may intro­ duce cross-modality noise after fusion and degrade the model’s
- Table 5: Effect of different 𝛼𝑣 values on performance over the LasHeR dataset.
- Table 6: Effect of Sharing Weights in the Backbone on Model Performance.
- Table 7: The impact of incorporating the CAM module into different baseline models on performance.

## 2026 PR CAST Curriculum Adaptation for One-Stream RGBT Tracking

图：
- Fig. 1: Intra-modal matching accuracy under diﬀerent training strategies, measured as the proportion of search-region locations whose attention responses exceed the mean value and fall inside the ground-truth bounding box.
- Fig. 2: Overall architecture of CAST. RGB and TIR inputs are processed within a unified transformer backbone, where our Dual-Expert Synergy (DES) modules enable modality-specific and shared expert learning through TopK routing. The right side illustrates the proposed four-stage curriculum adaptation strategy, which progressively stabilizes RGB anchoring, introduces TIR-specific adaptation, and finally achieves full multi-modal optimization.
- Fig. 3: Overall architecture of DES. RGB and TIR tokens are processed by modality-specific experts and shared experts under the control of a unified router. For each token, the router selects TopK experts according to learned scores, and only the selected experts contribute to the final output. Modality-specific experts preserve modality-unique knowledge, while the shared expert provides modality-general representations.
- Fig. 4: Success rate with diﬀerent attributes on LasHeR [38]. search image. We employ a four-stage curriculum adaptation (CA) training schedule. In the first three stages, the model is trained for 5 epochs each with a fixed learning rate of 10−4 to preserve modality-specific anchors and mitigate catastrophic forgetting. In the fourth stage, training proceeds for 15 epochs with an initial learning rate of 10−4 and a weight
- Fig. 5: Attention visualization of CAST with and without curriculum adaptation (CA). Without CA, the model’s attention is scattered and fails to consistently capture the target. With progressive CA training (Stages 1-4), the attention gradually converges toward the object, leading to more accurate and robust target localization.
- Fig. 6: Expert activation ratios between shared experts (orange) and modality-specific experts (blue) across DES layers under diﬀerent challenging scenarios. Results on low illumination, high illumination, hyaline occlusion, and thermal crossover show how the router dynamically balances shared and modality-specific experts to adapt to varying scene conditions. (For interpretation of the references to colour in this figure legend, the reader is referred to the web version of this article.)
- Fig. 7: Qualitative comparison between our method and other RGB-T trackers. The three sequences correspond to scenarios involving similar object interference, small target tracking, and fast motion. Our tracker maintains accurate and stable tracking results under all cases, demonstrating superior robustness and adaptability.

表：
- Table 1: Comparisons with state of the art trackers on the test set of LasHeR [38], RGBT234 [39], VTUAV-short [40] and VTUAV-long [40].
- Table 2: Comparisons with state of the art trackers on the test set RGBT210 [45].
- Table 3: Ablation study of proposed component. Δ denotes the average performance change compared to CAST in (M)SR and (M)PR.
- Table 4: Ablation study on the training order in curriculum adaptive training. Δ denotes the average performance change compared to CAST in (M)SR and (M)PR.
- Table 5: Eﬀect of routable expert number in DES under diﬀerent TopK settings.
- Table 6: Ablation study of DES positions. # Layers LasHeR RGBT234 3 9 15 21 SR PR MSR MPR
- Table 7: Ablation study on the number of training epochs in the four stages of curriculum adaptive (CA) training.
- Table 8: Comparison of inference speed and performance across diﬀerent models.

## 2026 PR Category Text-Guided RGBT Tracking

图：
- Fig. 1: The overall architecture of the proposed method. The RGBT tracking method with shared-specific feature representation primarily consists of three modules: the Position Guidance Module, the Hybrid Attention Module of Modality-shared and Modality-specific Features, and the Asymmetric Attention Module. The category text-guided RGBT tracking method includes the Category Text Generation Module and the Category Text Feature Guidance Module.
- Fig. 2: Architecture of the PGM. Illustrated using the RGB branch, this module integrates template frame features with normalized target coordinates. It encodes spatial information to generate position-enhanced template features, enabling the model to focus on the foreground target.
- Fig. 3: Overview of the HAM-SSF. The framework is composed of three parallel branches: RGB-specific, TIR-specific, and RGBT-shared feature extraction networks. These features are dynamically aggregated via the Modality Fusion Network using a hybrid attention mechanism to maximize cross-modal complementarity.
- Fig. 4: Schematic of the AAM. This module regulates the interaction between template and search frames to reduce redundancy. By employing an asymmetric attention mechanism, it eﬀectively suppresses background clutter and mitigates interference from similar distractors, ensuring precise target localization.
- Fig. 5: Illustration of the proposed category text-guided framework. (a) CTGM: Leverages the Grounding-DINO model to generate precise category text annotations from the template image. (b) CTFGM: Aligns the generated semantic text features with visual representations to guide the image branch, enhancing adaptability to target appearance variations.
- Fig. 6: Text generation examples from (a) RGBT234, (b) LasHeR, and (c) VTUAV. Each pair shows RGB (left) and TIR (right) images. performance evaluation metrics. PR measures the percentage of video frames where the distance between the center of the tracking result and the ground truth is less than a predefined threshold, which we set to 20.
- Fig. 7: The architecture of LTM. The module uses CLIP-ReID to match, identify and track the reappearance of the target.
- Fig. 8: Visual Comparison of Diﬀerent Tracking Methods on RGBT234 Dataset. Columns (a), (b), and (c) represent diﬀerent video sequences.
- Fig. 9: Visual Comparison of Diﬀerent Tracking Methods on LasHeR Dataset. Columns (a), (b), and (c) represent diﬀerent video sequences.
- Fig. 10: Visual Comparison of Diﬀerent Tracking Methods on VTUAV Dataset. Columns (a), (b), and (c) represent diﬀerent video sequences. into our model. Experimental results show that after integration, PR on VTUAV-LT increased from 61.5% to 63.6% (+2.1%) and SR from 53.3% to 54.2% (+0.9%). These results confirm that introducing text features into the image training process can further enhance the performance of the target tracking algorithm. We term this text-guided variant CTG-

表：
- Table 1: Quantitative comparisons on RGBT234 dataset. Higher values indicate better performance. The numbers with bold, underline, and italic indicate the best, the second best, and the third best
- Table 2: Quantitative comparisons on LasHeR dataset. Higher values indicate better performance.
- Table 3: Quantitative comparisons on VTUAV dataset. Higher values indicate better performance.
- Table 4: Ablation study on VTUAV-LT and VTUAV-ST. Baseline is included by default.

## 2026 PR Mining Representative Tokens for RGBT Tracking

图：
- Fig. 1: Comparison of our RGB-T tracker with previous transformer-based RGBT trackers.
- Fig. 2: The overall framework of our method. It primarily consists of a multi-modal separate-then-collaborative module and a cross-modal discrepancy constraint. Pattern Recognition 171 (2026) 112162 4
- Fig. 3: Illustration of the proposed triplet-attention block. and 𝐄R. Additionally, it is crucial to ensure that 𝐄R retains the ability to learn its global contextual information. The process can be expressed as follows: ̇ 𝐄R
- Fig. 4: Illustration of cross-modal discrepancy constraint. Pattern Recognition 171 (2026) 112162 5
- Fig. 5: The SR and PR scores of diﬀerent attributes on LasHeR [3] dataset. Best viewed in color. Pattern Recognition 171 (2026) 112162 7
- Fig. 6: Selection results visualized with and without CDC. Best viewed in color. Pattern Recognition 171 (2026) 112162 8
- Fig. 7: The figure indicates that non-representative tokens associated with irrelevant backgrounds gradually increase in the 1st, 5th, and 9th layers, although the diﬀerences are minimal. Combined with the results in Table 5, this suggests that inserting the MSC after the 1st transformer block is suﬃcient to select representative tokens eﬀectively. Notably, in the model configuration that achieves optimal performance, while most
- Fig. 8: Qualitative comparison of our tracker and other trackers on LasHeR [3] dataset. Pattern Recognition 171 (2026) 112162 9
- Fig. 9: Visualization of heat maps: (a) RGB search region, (b) RGB attention maps, (c) TIR search region, (d) TIR attention maps, and (e) final score maps. to precisely emphasize the target regions in both. Additionally, the final score maps demonstrate that our method excels in concentrating on the central regions of targets. These encouraging results confirm the capability of our approach to achieve robust complementary feature fusion across the two modalities.
- Fig. 10: Visualization of the success performance with respect to the FPS tracking speed on LasHeR [3].
- Fig. 11: Visualization of failure cases in our tracker. 5. Conclusion In this paper, we focus on addressing the performance degradation of RGB-T trackers caused by irrelevant background and modality gaps.

表：
- Table 1: Implementation and experimental settings. “lr” denotes learning rate.
- Table 2: Comparison with state of the art trackers on lasher [3] and vtuav [4] datasets. Higher values indicate better performance. The best two results are shown in bold and italic fonts.
- Table 3: Comparison with state of the art methods on RGBT234 [15] dataset and RGBT210 [14] dataset. The best two results are shown in bold and italic fonts.
- Table 4: Ablation studies for MRTTrack on LasHeR [3] dataset. Method PR (↑) NPR (↑) SR (↑) FlOPs (G) Params (M) FPS (↑) Baseline tracker 68.94 65.32 55.12 63.70 109.83 48.3 +MSC 69.96 (+1.02) 66.20 (+0.88) 56.15 (+1.03) 77.29 131.09 32.5
- Table 5: Ablation study on the insertion of MSC module on LasHeR [3] dataset.
- Table 6: Ablation with the diﬀerent values of parameter 𝛾 on LasHeR [3] dataset.
- Table 7: Evaluation results under diﬀerent random seeds on LasHeR [3] dataset.

## 2026 PR RGBT Tracking via Supervised Mutual Guiding

图：
- Fig. 1: Visualization of positive and negative sample feature distributions using t-SNE technology. Herein, SMGNet w/o weight denotes our SMGNet without mutual guiding weights. DMCNet [8] and BAT [9] are two representative mutual guiding-based RGBT trackers. Positive and negative samples are generated through a Gaussian distribution centered around the ground truth. Positive samples have an IoU greater than 0.7 with the ground truth, while negative samples have an IoU smaller than 0.3, consistent with the settings in MDNet [10].
- Fig. 2: The overall framework of our SMGNet. Firstly, RGB and TIR image patches are transformed into tokens and processed by two-stream weight shared Vision Transformer (ViT) for joint feature extraction and intra-modal search-template matching. The multi-modal search region tokens are then fed into a Classification-based Reliability Estimating Module (CREM) to estimate the reliability weights for each modality. Subsequently, cross-modal interaction performs through an Adaptive Mutual Guidance Module (AMEM), leveraging the estimated reliability weights to facilitate complementary information propagation between diﬀerent modalities.
- Fig. 3: Illustration of the eﬀectiveness of our estimated reliability weights compared to three typical attention-based RGBT trackers. Top: Curves of the reliability weights predicted by ours compared to several typical RGBT trackers. Bottom: Comparison of our tracking results against FANet, MaCNet and SiamTFA.
- Fig. 4: The detailed architecture of adaptive mutual guidance module. We omit the operations like LN and MLP for clear presentation.
- Fig. 5: Latency analysis. Visualization of the runtime latency percentages of ViT, CREM, AMGM, and the Head.
- Fig. 6: Attribute-based evaluation on the LasHeR dataset. For clarity, only the minimum and maximum values for each attribute metric are presented. Track+RGBT. However, SMGNet exhibits significant performance improvements over OSTrack+RGBT across all five RGBT tracking datasets, making these additional overheads acceptable.
- Fig. 7: Failure cases. Our SMGNet shows diﬃculty in predicting accurate bounding boxes in occlusion and similar interferential object conditions. Better viewed in color with zoom-in.
- Fig. 8: Qualitative comparison of SMGNet against five state of the art trackers on four video sequences.
- Fig. 9: Qualitative comparison of SMGNet against diﬀerent variants trackers on two video sequences. Pattern Recognition 171 (2026) 112295 10

表：
- Table 1: The MPR, MSR, PR, NPR, and SR scores (%) of diﬀerent trackers on five datasets. The highest and second-best results are highlighted in bold and italic respectively. * indicates that the tracker has been re-trained using the LasHeR/VTUAV training set.
- Table 2: Comparison about the FLOPs, Params and Speed(fps). Algorithms FLops(G) Params(M) Speed(fps) OSTrack+RGBT 59.161 102.740 60.6 SMGNet 67.936 134.857 41.4
- Table 3: Compared to our SMGNet, SMGNet-add exhibits a significant performance degradation across all datasets and evaluation metrics. This degradation can be attributed to the distribution gap present in multimodal data. Therefore, it is crucial to design a suitable transformation method, as demonstrated by the eﬀectiveness of the designed AMGM in
- Table 4: The MPR, MSR, PR, NPR, and SR scores (%) of diﬀerent variants with diﬀerent numbers of binary classifiers on four datasets. The highest and second-best results are highlighted in bold and italic respectively.
- Table 5: The MPR, MSR, PR, NPR, and SR scores (%) of diﬀerent variants of multimodal fusion methods on four datasets.

## 2026 PR Temporal Multimodal Knowledge Distillation for Modality-Missing RGBT Tracking

图：
- Fig. 1: Comparison of feature visualizations and tracking results between the baseline (BAT[8] tracker without any distillation modules) method and our proposed cross-frame relation distillation module (CRDM) approach. The baseline exhibits inconsistent and scattered features across frames, while our method, by distilling cross-frame relations, achieves well-localized and consistent responses. The tracking results are annotated with bounding boxes: green denotes the ground truth, blue indicates the baseline predictions, and red represents our method’s predictions. The dashed box in the figure represents the missing modality.
- Fig. 2: An overview of our proposed modality-missing RGBT tracking framework based on a knowledge distillation (TMKD). It contains a teacher and a student tracker, which take complete multimodal data and modality-missing data as the input, respectively. The missing modality data is imputed by copying from the available modality. These two networks share the same architecture, i.e., tracking using a unified Transformer backbone network similar to BAT[8].
- Fig. 3: Visualization of the eﬀectiveness of the novel multi-level distillation framework of CRDM, DFD, and LRD in enhancing feature discrimination. The dashed box in the figure represents the missing modality.
- Fig. 4: Ablation studies of key factors aﬀecting TMKD performance. (a) Precision Rate (PR) variation across scenarios on four datasets under a diﬀerent alignment weight α in DFD. (b) Performance comparison on RGBT234 and LasHeR datasets under diﬀerent missing rates of ρ.
- Fig. 5: Qualitative comparison under representative missing-pattern challenges on the LasHeR dataset. RM: Random Missing, LTM: Long Time Missing, SM: Switch Missing, LTMM: Long Time Mixed Missing, SMM: Switch Mixed Missing.
- Fig. 6: Qualitative comparison between TMKD and other advanced trackers on six representative sequences.
- Fig. 7: Visualization of features of diﬀerent models. (a) TBSI/copy, (b) IPL with missing modalities, (c) TMKD with missing modalities, (d) TMKD with complete modalities.
- Fig. 8: Visualization display of tracking results for diﬀerent models with missing modalities. The green rectangles denote ground truth in the template frame. Our TMKD shows the best performance in diﬀerent frame sequences.
- Fig. 9: Failure cases on three representative sequences from datasets. that the DFD loses the complementary information from the missing modality, making it harder to capture weak diﬀerences between objects with similar appearances. Meanwhile, since the CRDM relies on the object prototype feature from diﬀerent frames, when one modality misses, this prototype becomes less distinctive compared with other dense and similar-looking objects, causing ambiguous cross-frame correlations. Our

表：
- Table 1: : Comparison with state of the art methods on RGBT234 and LasHeR testing set for modalitycomplete and modality-missing scenarios.The best, second best, third best, and fourth best results are highlighted in red, blue, cyan, and orange, respectively.
- Table 2: : Comparison with state of the art methods on VTUAV and VTUAV176-Miss datasets. The best and second best results are labeled in red and blue colors, respectively.
- Table 3: : Ablation study of CRDM, DFD, and LRD, analyzing the individual contribution of each component and their interactions. The best results are labeled in red.
- Table 4: : Sensitivity analysis of the sampling size m in the sequence loading strategy. The best results are labeled in red.

## 2026 RIE SiamCCA Collaborative Channel-Spatial Aggregation for RGBT Tracking

图：
- Fig. 1: The overall network architecture of SiamCCA. The backbone is a triple-stream structure. Among this, dynamic gating scale awareness (DGSA) module and channel-spatial collaborative aggregation (CSCA) module are for single-modal feature extraction and multi-modal feature fusion, respectively. Region proposal selection (RPS) module is for optimal proposal selection.
- Fig. 2: Detailed architecture of the dynamic gating scale awareness (DGSA) module. “LN” denotes layer normalization, “DWConv” refers to depthwise convolution, and “PWConv” indicates pointwise convolution.
- Fig. 3: Detailed architecture of the channel-spatial collaborative aggregation (CSCA) module. “G” denotes the divided groups; “X Avg Pool” and “Y Avg Pool” represent horizontal and vertical average pooling operations, respectively.
- Fig. 4: Comparison of PR and SR metric between SiamCCA and 12 excellent RGBT trackers on the GTOT dataset.
- Fig. 5: Comparison of PR and SR metric between SiamCCA and 9 excellent RGBT trackers on the RGBT234 dataset. are cropped based on the target’s position in the previous frame, and the target’s position in the current frame is inferred through subsequent network modules.
- Fig. 6: PR and SR metric based on attribute challenge on the GTOT dataset. and DAPNet [8], our tracking speed is more than 30 times faster than theirs.
- Fig. 7: The RGBT23 dataset is utilized to conduct a qualitative comparison on the car4, elecbike10, supbus2 and manwithbasketball video sequences with four exceptional trackers.
- Fig. 8: Visual analysis of the channel-spatial collaborative aggregation (CSCA) module shows that our approach demonstrates strong robustness against environmental disturbances, yielding higher localization accuracy.
- Fig. 9: Visual analysis of the dynamic gating scale awareness (DGSA) module shows that the proposed strategy can help the backbone network pay more attention to the target region.
- Fig. 10: The regional proposal selection (RPS) module selects the optimal proposal by comparing the confidence scores of visible and infrared images.
- Fig. 11: Comparison of PR (%) and speed metrics between SiamCCA and 7 RGBT trackers on the GTOT dataset.
- Fig. 12: Comparison of PR (%) and speed metrics between SiamCCA and 7 RGBT trackers on the RGBT234 dataset.
- Fig. 13: Failure cases of the minibusnig and running sequences in the RGBT datasets.

表：
- Table 1: Comparison results of SiamCCA and other trackers on GTOT and RGBT234 datasets.
- Table 2: PR/SR (%) analysis of SiamCCA and seven state of the art algorithms on RGBT234 dataset based on attributes.
- Table 3: Comparison results of SiamCCA and its variants on GTOT and RGBT234 datasets. “✓” indicates the addition of the corresponding network module.

## 2026 TIP Causality-Based Modality and Platform Invariant Representation for Dynamic RGBT Tracking

图：
- Fig. 1: (a) Represents the conventional RGBT tracking paradigm, where the tracker fails to accurately track the target once it is completely occluded.
- Fig. 2: A causal graph of dynamic RGBT tracking. The arrow indicates a causal relationship between the two factors. X denotes the input images, T represents the target-relevant information, B indicates the output bounding box, and M refers to the target-irrelevant information (i.e., modality/platform information).
- Fig. 3: The overall framework of the proposed method consists of a causality-inspired dynamic tracker and a platform-independent global searcher. the global searcher during the training process, we adapt a two-stage training strategy. In the first stage, we initially train the dynamic tracker. Specifically, we employ a Causal Consistency Encoder (CCE) with a style intervener to replace the original encoder for extracting modality-invariant features,
- Fig. 4: Visualization of feature maps and response maps. “+intervener” denotes the feature maps and the predicted center-point response maps obtained after applying interventions to the features, and the numbers on the response maps indicate the confidence strength.
- Fig. 5: A schematic diagram illustrating the workflow of the dynamic tracking framework in the testing phase. and employ causal consistency loss for regularization. The network architecture of the global searcher is illustrated in
- Fig. 6: The distribution of object categories and challenging attributes in the dataset.
- Fig. 7: The drones and handheld cameras used for data collection. platform variations during tracking to capture robust target representations.
- Fig. 8: Distribution of object sizes in the DRGBT603 dataset. handheld cameras as platforms to collect data. The sequence pairs from different modalities are then aligned first, with the specific operations consistent with previous work [9].
- Fig. 9: Sequences synthesized based on existing tracking data. visualize the distribution of target sizes, as shown in Figure 8.
- Fig. 10: Evaluation result on DRGBT603 testing set using precision, normalized precision and success plots, where the representative scores are presented in the legend.
- Fig. 11: Visualization of the modality distribution comparison between synthetic and real data on the DRGBT603 test set.
- Fig. 12: Visualization of the differences in challenge categories between real data and synthetic data on DRGBT603.
- Fig. 13: Quantitative comparison between the proposed method and other trackers on the DRGBT603 dataset.
- Fig. 14: Comparison of attention visualizations between the proposed method and the baseline (OSTrack with DropMAE as the pretrained weights).
- Fig. 15: T-SNE visualization comparison of feature maps between the baseline method (OSTrack with DropMAE as the pretrained weights) and the proposed method. For T-SNE maps, they have the same scale of axes.
- Fig. 16: T-SNE visualization comparison under failure and success modes. For the T-SNE maps, the axes share the same scale.

表：
- Table I: COMPREHENSIVE COMPARISON OF RGBT TRACKING DATASETS. THE X AND × SYMBOLS INDICATE PRESENCE OR ABSENCE, RESPECTIVELY efficiently transfer the performance of RGB trackers to RGBT tracking tasks through fine-tuning. BAT [13] designs a simple bidirectional adapter for feature fusion between the two
- Table II: LIST OF ATTRIBUTES ANNOTATED IN DRGBT603
- Table III: ATTRIBUTE-BASED PRECISION AND SUCCESS SCORES OF 7 TRACKERS ON DRGBT603.
- Table IV: PR, NPR, AND SR SCORES OF 8 TRACKERS ON REAL AND SYNTHETIC DATA. THE BEST AND SECOND ARE THE RESULT OF THE RED AND THE GREEN Precision Rate) and SR (Success Rate), respectively. Our
- Table V: COMPARISON OF METHODS INITIALIZED WITH DROPMAE PRE-TRAINED WEIGHTS. FOR EACH METHOD, THE RESULTS ARE REPORTED USING THE MODEL PARAMETERS OBTAINED FROM THE LAST THREE TRAINING EPOCHS
- Table VI: COMPONENT ANALYSIS ON DRGBT603 DATASET
- Table VII: REPLACING LAYERS OF THE PROPOSED CCE target features are subtle, several methods fail to maintain stable tracking when only RGB modality is available. After platform switching, these methods become subject to inter-
- Table VIII: PERFORMANCE ANALYSIS OF REPLACING CCE AT ANY FOUR LAYERS
- Table IX: ANALYSIS OF HYPERPARAMETERS σ determine the optimal setting for σ, we perform experiments on the DRGBT603 testing set. As shown in Table IX, it can be observed that the overall performance of the proposed method
- Table X: ANALYSIS OF HYPERPARAMETERS λ3 ON DRGBT603 DATASET method, we conduct an ablation study. As shown in Table X, the proposed method achieves the best performance when the hyperparameter λ3 is set to 1.
- Table XI: PERFORMANCE COMPARISON ACROSS CHALLENGE CATEGORIES UNDER DIFFERENT TRAINING SETTINGS. REAL DENOTES TRAINING USING ONLY REAL DATA, SYNTHETIC DENOTES TRAINING USING ONLY SYNTHETIC DATA, AND FULL DENOTES TRAINING USING ALL AVAILABLE TRAINING DATA
- Table XII: CROSS-DATASET EVALUATION. † INDICATES THE DATASET AFTER SIMULATED DYNAMIC VARIATION PROCESSING It can be observed that when trained using only real or synthetic data, our method outperforms the baseline in the CV
- Table XIII: COMPARATIVE ANALYSIS BETWEEN SYNTHETIC AND REAL DATA. REAL DENOTES TRAINING USING ONLY REAL DATA, SYNTHETIC DENOTES TRAINING USING ONLY SYNTHETIC DATA, AND FULL DENOTES TRAINING USING ALL AVAILABLE TRAINING DATA
- Table XIV: INFERENCE SPEED & GPU MEMORY USAGE. T-FPS DENOTES THE TRACKING FPS, WHILE R-FPS DENOTES THE RE-LOCALIZATION FPS

## 2026 TMM Scale-Aware Attention and Multimodal Prompt Learning for RGBT Tracking

图：
- Fig. 1: Comparison of the proposed method on the LasHeR dataset with existing state of the art trackers in terms of precision and tracking speed. Color display is recommended for best viewing.
- Fig. 2: Overall architecture of the proposed method MPANet. foreground masks and history visual features to provide comprehensive and accurate prompt information for the Siamese tracker. EVPTrack [41], meanwhile, introduced an explicit visual prompt tracking framework, which generated explicit optical visual prompts through spatial-temporal tokens to assist the
- Fig. 3: Scale-aware dilation attention. while achieving effective feature fusion through cross-attention mechanisms, promoting complementarity between RGB and TIR modal features. This hierarchical fusion strategy enables to achieve feature fusion for different purposes at different stages, fully considering the characteristics of multi-modal tracking
- Fig. 4: Multi-modal prompts interaction learning module.
- Fig. 5: Submodules in multi-modal prompts interaction learning. through linear layers to generate query Q, key K, and value V . Considering the dynamic nature of target scale variations in RGBT tracking, dilated convolution kernels with three different dilation rates r = 1, 2, 3 are designed to process K and V , obtaining keys Kr and values Vr with different receptive fields:
- Fig. 6: Cross-fusion adapter. function. yma = cat[maxpool(y), avgpool(y)] (13) SA(y) = Sigmoid(conv(yma)) (14) This classical spatial attention design has proven its effectiveness in visual tracking tasks, enabling the model to extensively
- Fig. 7: Evaluation results of PR and SR scores for different attributes on GTOT dataset for MPANet with seven trackers.
- Fig. 8: Precision rate (PR) and success rate (SR) evaluation curves of MPANet with 8 trackers on LasHeR dataset.
- Fig. 9: Visual comparison of MPANet with seven trackers in the Car and elecbikewithlight1 sequences on RGBT234 dataset.
- Fig. 10: Visual comparison of MPANet with seven trackers in the ab_blkskirtgirl and carlightcome2 sequences on LasHeR dataset.
- Fig. 11: Failure cases of MPANet in 3rdfatboy and 3rdgrouplastboy sequences on LasHeR dataset.

表：
- Table I: EXPERIMENT ENVIRONMENT AND TRAINING PARAMETER SETTINGS proposed method on the RGBT benchmark dataset. To be specific, PR is defined as the proportion of all frames in which the distance between the centre of the predicted box and the cen-
- Table II: COMPARISON RESULTS OF THE PROPOSED MPANET WITH STATE-OF-THE-ART METHODS ON GTOT, RGBT234 AND LASHER BENCHMARK TRACKING DATASETS.
- Table III: COMPARISON OF PR SCORES BETWEEN THE PROPOSED MPANET AND THE STATE-OF-THE-ART METHOD FOR DIFFERENT ATTRIBUTES ON RGBT234 DATASET.
- Table IV: COMPARISON OF SR SCORES BETWEEN THE PROPOSED MPANET AND THE STATE-OF-THE-ART METHOD FOR DIFFERENT ATTRIBUTES ON RGBT234 DATASET.
- Table V: COMPARATIVE RESULTS OF PERFORMANCE EVALUATION ON SHORT-TERM AND LONG-TERM SUBSETS OF VTUAV DATASET method. Against DAFNet and ADRNet, MPANet exhibits more substantial tracking performance gains. These results indicate
- Table VI: PARAMETERS, FLOPS, MODEL SIZE, AND LASHER DATASET PERFORMANCE COMPARISON RESULTS of model scale and computational efficiency. Regarding parameter count, MPANet contains 123.42 M parameters, which is
- Table VII: RESULTS OF ABLATION EXPERIMENTS OF MPANET AND VARIANTS THEREOF ON LASHER DATASET
- Table VIII: RESULTS OF ABLATION EXPERIMENTS FOR EACH COMPONENT OF MPIL ON LASHER DATASET The ablation study results demonstrate that the baseline model achieves 68.9% PR and 55.0% SR on the LasHeR dataset, with
- Table IX: RESULTS OF ABLATION EXPERIMENTS WITH DIFFERENT COMBINATIONS OF DUAL-BRANCH OUTPUT FEATURES which are 1.7% and 1.1% lower compared to those of the complete MPIL model, respectively. This discrepancy proves the

## 2026 TMM Video-Level Cross-Modal Temporal Navigation for RGBT Tracking

图：
- Fig. 1: Differences between the two image-level methods and our videolevel method. (a) Image-level full fine-tuning methods employ the RGBbased pre-trained model to extract multi-modal features, mainly relying on the history frames for capturing temporal information. (b) Image-level prompttuning methods leverage modality prompts instead of the modal-specific fusion module, and capture temporal information by the online template branch. (c)
- Fig. 2: Overall architecture of our proposed VCT. Firstly, the temporal prompts, the template video-clip patch embeddings, and the current search patch embeddings are fed into the L-layer encoders. Then, the MS-MoA module enables the cross-modal spatio-temporal adaptive fusion, and the CM-TPN module establishes intra-modal inter-frame temporal dependencies to guide subsequent frame inferences. Finally, the output of the last encoder is forwarded to the box head for obtaining the prediction results.
- Fig. 3: Illustration of the CM-TPN. The CM-TPN generates enhanced temporal prompts through the PEFT methods, and uses the multi-head attention to aggregate and compress the enhanced temporal prompts for obtaining modality-specific temporal information.
- Fig. 4: Illustration of the MS-MoA. It is composed of modality-specific routers functioning as sparse gating mechanisms and the parameter-shared mixture of adapters (MoA) as experts.
- Fig. 5: Precision rate and success rate of different attributes on the LasHeR [46] test set.
- Fig. 6: Visualization results of five competitive trackers and our tracker on six sequences with different challenging attributes from the LasHeR [46] benchmark. (a) 7rightorangegirl (LR, BC, TC, SV). (b) AQgirlwalkinrain (MB, BC, CM, FM). (c) bikeboyintodark (LI, SA, TC, ARC). (d) boywalkinginsnow2 (PO, DEF, BC, TC). (e) darktreesboy (MB, LI, LR, TC). (f) manoncall (TO, BC, CM, SV).
- Fig. 7: Visualization of the limitations of our proposed method. (a) 1stcol4thboy (LR, SA, FL, ARC). (b) abwhiteboywithbluebag (TO, BC, TC, OV).

表：
- Table I: PERFORMANCE COMPARISONS ON THE LASHER [46], RGBT210 [47], AND RGBT234 [20]. THE BEST THREE RESULTS ARE HIGHLIGHTED IN RED, BLUE, AND GREEN, RESPECTIVELY.
- Table II: COMPARISON WITH THE STATE-OF-THE-ARTS ON THE GTOT [50]. THE BEST THREE RESULTS ARE HIGHLIGHTED IN RED, BLUE, AND GREEN, RESPECTIVELY.
- Table III: ABLATION STUDIES ON THE EFFECT OF THE COMPONENTS ON THE LASHER [46] DATASET. CM-TPN AND MS-MOA DENOTE THE CROSS-MODAL TEMPORAL PROMPT NAVIGATOR AND THE MODALITY-SPECIFIC MIXTURE OF ADAPTERS, RESPECTIVELY.
- Table IV: QUANTITATIVE COMPARISONS OF PR AND SR SCORES UNDER THE CHALLENGING ATTRIBUTES ON THE LASHER [46] TEST SET.
- Table V: ABLATION STUDY ON TEMPORAL PROMPT STRATEGIES FOR CM-TPN ON THE LASHER DATASET.
- Table VI: ABLATION STUDY ON THE MODALITY-SPECIFIC MIXTURE OF ADAPTERS (MS-MOA) ON THE LASHER DATASET.
- Table VII: PERFORMANCE COMPARISON ON DIFFERENT CHALLENGES. Challenge Tracker LasHeR [46] PR (↑) SR (↑)
- Table VIII: COMPARISON ON COMPUTATIONAL COST AND INFERENCE SPEED WITH ADVANCED TRACKERS ON LASHER. ‘*’ DENOTES THAT THE SPEED OF THE METHOD IS CITED FROM ITS ORIGINAL PAPER AS THE CODE AND MODELS ARE UNAVAILABLE.
