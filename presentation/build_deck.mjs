// Optional Artifact Tool authoring script. Scientific Python runs do not need it.
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL, fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { Presentation, PresentationFile } from '@oai/artifact-tool';

const ROOT = process.env.MM_REPO_ROOT ?? path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const BUILD = process.env.MM_DECK_BUILD ?? path.join(ROOT, 'results/deck-build');
const SKILL = '/root/.codex/skills/builtins/presentations';
const FONT = 'DejaVu Sans';
const BLUE = '#145A81', INK = '#172D3C', MUTED = '#566773', ORANGE = '#B85225';
const data = JSON.parse(await fs.readFile(path.join(ROOT, 'presentation/data/draft_results.json'), 'utf8'));
// Excel-backed native charts store at most 15 significant decimal digits.
// Use 12 for display; the full-precision scientific source remains unchanged.
const displayNumber = n => Number(Number(n).toPrecision(12));
const evidence = data.summary.thresholds_and_msy;
const p = Presentation.create({ slideSize: { width: 1280, height: 720 } });
await fs.mkdir(path.join(BUILD, 'previews'), { recursive: true });

function text(s, name, value, x, y, w, h, size=28, bold=false, color=INK) {
  const t=s.shapes.add({geometry:'textbox',name,position:{left:x,top:y,width:w,height:h},fill:'none',line:{style:'solid',fill:'none',width:0}});
  t.text=value;
  t.text.style={typeface:FONT,fontSize:size,bold,color,insets:0,wrap:'square',autoFit:'none',verticalAlignment:'top'};
  return t;
}
function slide(title, notes) {
  const s=p.slides.add();s.background.fill='#FFFFFF';
  text(s,'heading',title,70,45,1140,105,44,true);
  text(s,'draft-footer','Working draft, synthetic examples',70,674,1100,25,17,false,MUTED);
  s.speakerNotes.text=notes;
  return s;
}
function chartStyle() {
  return {chartFill:'#FFFFFF',chartLine:{style:'solid',fill:'none',width:0},plotAreaFill:'#FFFFFF',plotAreaLine:{style:'solid',fill:'none',width:0},hasLegend:true,legend:{position:'bottom',overlay:false,textStyle:{typeface:FONT,fontSize:18}},titleTextStyle:{typeface:FONT,fontSize:24,color:INK}};
}
const source='WP03 source: artifacts/tables/wp03_thresholds.csv; artifacts/tables/wp03_event_validation.csv; artifacts/manifests/wp03_summary.json. Source branch dependency: PR #4, commit 20fbd5b21844a94e81e021d1571fbed0f7b47379. All examples synthetic.';

{
  const s=p.slides.add();s.background.fill='#FFFFFF';
  text(s,'title','Harvesting under a\nstrong Allee effect',70,125,1130,205,64,true,BLUE);
  text(s,'subtitle','Collapse thresholds and PINN analysis',74,370,1100,70,34);
  text(s,'authors','RaghavSinghal15, AshChan07, devam2006\nPrem-Mehta03, rohanagrawal28',74,490,1100,85,25,false,MUTED);
  text(s,'draft-footer','Working draft, 28 October 2026',74,674,1100,25,17,false,MUTED);
  s.speakerNotes.text='Approved full title: Harvesting under a Strong Allee Effect: Collapse Thresholds, Hysteresis and Comparison of Constant-Yield vs Proportional-Effort Harvesting, with Physics-Informed Neural Network (PINN) Forward and Inverse Analysis. Partial group draft. Final talk is 25 minutes plus 5 minutes Q&A. Actual presentation date and author names still need confirmation. '+source;
}
{
  const s=slide('Models and scaling','Explain the low-density Allee factor before harvesting. N/K is population as a fraction of carrying capacity; tau=rt rescales time. H has population/time units; h has inverse-time units. Inverse fitting uses declared fixed scales when true r or K is hidden. Approved proposal and docs/SCIENTIFIC_CONTRACT.md.');
  text(s,'model-a-label','Constant catch',72,170,1100,40,27,true,BLUE);
  text(s,'model-a','A: x′ = x(1 − x)(x/a − 1) − q',72,220,1100,60,35);
  text(s,'model-b-label','Proportional effort',72,315,1100,40,27,true,BLUE);
  text(s,'model-b','B: x′ = x(1 − x)(x/a − 1) − ex',72,365,1100,60,35);
  text(s,'scales','x = N/K     τ = rt     a = A/K\nq = H/(rK)     e = h/r',72,475,1100,90,28);
  text(s,'assumptions','One deterministic population, constant parameters, 0 < A < K',72,601,1100,40,24,false,MUTED);
}
{
  const s=slide('Equilibria and harvesting history','Draft slots for WP01 and WP02. Do not present pending results as measured. WP01 needs its corrected/restored PR, including numerical review fixes. WP02 needs both fair comparison protocols and two ramp speeds with continuous state and explicit restocking. Sources: docs/tasks/WP01_foundations.md and WP02_model_b.md.');
  text(s,'wp01-title','WP01: foundations and Model A',72,180,1120,50,31,true,BLUE);
  text(s,'wp01-pending','Awaiting the corrected equilibrium, stability\nand branch-diagram contribution',72,245,1120,115,29);
  text(s,'wp02-title','WP02: comparison and harvesting history',72,405,1120,50,31,true,BLUE);
  text(s,'wp02-pending','Awaiting matched-policy comparisons, harvest ramps\nand explicitly labelled restocking experiments',72,470,1120,115,29);
}
{
  const s=slide('Harvesting thresholds',source+' Derive A by maximising production g(N). Derive B by maximising production per individual. The thresholds have different units and must not be compared directly as policy-risk scores. At either positive fold the equilibrium is semistable.');
  text(s,'parameters','Illustrative parameters: r = 0.7, K = 100, A = 20',72,139,1120,38,25,false,MUTED);
  const values=[['Quantity','Value','Units'],['A: N*',evidence.N_star.toFixed(5),'Population'],['A: Hc',evidence.H_c.toFixed(5),'Population / time'],['B: hc',evidence.h_c.toFixed(2),'1 / time'],['Logistic: Hc',evidence.H_c_logistic.toFixed(1),'Population / time']];
  const table=s.tables.add({rows:5,columns:3,left:72,top:203,width:1136,height:300,columnWidths:[400,280,456],values});
  table.borders.assign({style:'solid',fill:'#D5DFE5',width:1});
  for(let r=0;r<5;r++)for(let c=0;c<3;c++){
    const cell=table.getCell(r,c);cell.fill=r===0?BLUE:'#FFFFFF';
    cell.text.style={typeface:FONT,fontSize:27,bold:r===0,color:r===0?'#FFFFFF':INK,insets:12};
  }
  text(s,'interpretation','A maximises total growth. B maximises growth per individual.\nA population barrier still matters below either threshold.',72,548,1136,95,27);
}
{
  const s=slide('Initial population separates the outcomes',source+' Branch curves are generated by scripts/build_presentation_data.py using the implemented basin API, with each model at the same fraction of its own control threshold. This is a threshold-normalised comparison, not equal realised catch. At the fold only the upper side is attracted. A zero at positive catch is a termination policy, not an equilibrium.');
  for(const [model,left] of [['A',62],['B',690]]){
    const b=data.branches[model];
    s.charts.add('scatter',{...chartStyle(),position:{left,top:166,width:520,height:405},title:'Model '+model,scatterOptions:{style:'line'},series:[
      {name:'Lower unstable barrier',xValues:b.control_fraction.map(displayNumber),values:b.lower.map(displayNumber),line:{style:'solid',fill:ORANGE,width:3},marker:{symbol:'none'}},
      {name:'Upper stable branch',xValues:b.control_fraction.map(displayNumber),values:b.upper.map(displayNumber),line:{style:'solid',fill:BLUE,width:3},marker:{symbol:'none'}}
    ],xAxis:{title:{text:model==='A'?'H / Hc':'h / hc',textStyle:{typeface:FONT,fontSize:22}},min:0,max:1,majorUnit:.25,textStyle:{typeface:FONT,fontSize:18},numberFormatCode:'0.00'},yAxis:{title:{text:'x = N / K',textStyle:{typeface:FONT,fontSize:22}},min:0,max:1.1,majorUnit:.2,textStyle:{typeface:FONT,fontSize:18},numberFormatCode:'0.0',majorGridlines:{style:'solid',fill:'#E1E7EB',width:1}}});
  }
  text(s,'basin-interpretation','Below the lower branch: collapse. Above it: approach the upper branch.\nAt the fold, attraction occurs only from above.',72,590,1136,70,25);
}
{
  const s=slide('A reaches zero in finite time',source+' The six case indices follow rows in wp03_event_validation.csv. Values are dimensionless extinction times. Integral evaluation uses quadrature or an elementary fold antiderivative; DOP853 integrates an independently expanded polynomial. Largest default disagreement among both RK45 settings, integral evaluation and DOP853 is below 4.6e-8. RK45 uses Dormand-Prince 5(4), as documented at https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.solve_ivp.html .');
  text(s,'integral','τ_ext = ∫ [q − G(u)]⁻¹ du\nfrom 0 to x₀',72,180,535,100,31,true,BLUE);
  text(s,'integral-rule','Only reaching-zero paths\nenter the integral.',72,321,535,90,28);
  text(s,'event-rule','RK45 stops at the first\ndownward zero crossing.',72,440,535,90,28);
  text(s,'b-rule','B extinction paths approach zero asymptotically.',72,570,550,70,26);
  s.charts.add('bar',{...chartStyle(),position:{left:660,top:169,width:550,height:450},title:'Independent checks',barOptions:{direction:'column',grouping:'clustered',gapWidth:95},categories:data.events.map((_,i)=>String(i+1)),series:[{name:'Integral evaluation',values:data.events.map(r=>displayNumber(r.quadrature_tau)),fill:BLUE},{name:'Independent DOP853',values:data.events.map(r=>displayNumber(r.dop853_tau)),fill:ORANGE}],xAxis:{title:{text:'Finite case',textStyle:{typeface:FONT,fontSize:22}},textStyle:{typeface:FONT,fontSize:20}},yAxis:{min:0,title:{text:'Extinction time τ',textStyle:{typeface:FONT,fontSize:22}},textStyle:{typeface:FONT,fontSize:19},majorGridlines:{style:'solid',fill:'#E1E7EB',width:1}}});
}
{
  const s=slide('Forward and inverse PINN evidence','Pending WP04/WP05 contributions. Do not claim scores or parameter recovery before actual runs arrive. Forward comparison needs independent A/B numerical references, error/runtime and failure cases. Inverse comparison needs known-K identifiability design, frozen observations/splits, ODE-fit baseline and held-out/noise evidence. Sources: docs/tasks/WP04_forward_pinn.md and WP05_inverse_pinn.md; docs/SCIENTIFIC_CONTRACT.md.');
  text(s,'forward-title','WP04: forward problem',72,185,545,55,31,true,BLUE);
  text(s,'forward-pending','Awaiting actual A/B predictions,\nRMSE and relative error,\nruntime and near-collapse failure',72,269,545,180,28);
  text(s,'inverse-title','WP05: inverse problem',660,185,550,55,31,true,BLUE);
  text(s,'inverse-pending','Awaiting parameter recovery,\nnoise and held-out validation,\nand an ODE-fitting baseline',660,269,550,180,28);
  text(s,'pending-note','No numerical PINN result is included in this draft.',72,555,1136,70,27,false,MUTED);
}
{
  const s=slide('Classical findings and limits',source+' These are the supported partial conclusions. Add WP02 policy/history evidence and WP04/WP05 measured findings after review. No species-specific or field-data validation exists. Code and exposition used OpenAI ChatGPT/Codex assistance, recorded in docs/AI_USAGE.md. Each member must check and understand their own contribution.');
  text(s,'finding-1','Initial population matters even below the harvesting cliff.',72,179,1136,80,32,true,BLUE);
  text(s,'finding-2','Fixed catch can cause finite-time extinction.\nOn extinction paths, B approaches zero asymptotically.',72,292,1136,120,31);
  text(s,'finding-3','A long bottleneck can hide an eventual collapse.',72,442,1136,80,31);
  text(s,'limitation','These conclusions concern the assumed deterministic model.\nAll current examples are synthetic. PINN validation is pending.',72,565,1136,85,25,false,MUTED);
}
{
  const s=slide('Questions','Reserve five minutes in the final presentation. Questions to rehearse: Why is zero not an A equilibrium at positive catch? Why classify before integration? What is RK45 5(4)? How are tolerances checked independently? What makes a fold semistable? Why can good inverse trajectory fit coexist with poor parameter recovery? Do not claim rehearsal or human understanding has already happened.');
  text(s,'question-subtitle','Thresholds, basins, extinction\nand numerical checks',72,245,1120,150,44,false,BLUE);
  text(s,'question-timing','Final allocation: 25-minute talk and 5-minute Q&A',72,520,1120,70,28);
}

const { finalizePresentation } = await import(pathToFileURL(path.join(SKILL,'container_tools/artifact_tool_utils.mjs')).href);
const candidate=path.join(BUILD,'candidate.pptx');
await fs.mkdir(path.join(BUILD,'versions'),{recursive:true});
await fs.mkdir(path.join(BUILD,'receipts'),{recursive:true});
const revision=Date.now();
const validated=path.join(BUILD,'versions',`draft-${revision}.pptx`);
const receipt=path.join(BUILD,'receipts',`draft-${revision}.validation.json`);
await (await PresentationFile.exportPptx(p)).save(candidate);
await finalizePresentation({workspaceDir:path.dirname(ROOT),candidatePath:candidate,finalPath:validated,pythonExecutable:process.env.CODEX_PRIMARY_RUNTIME_PYTHON,integrityValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(SKILL,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit','--require-native-table-slide','4'],requiredNativeTableOwnerSlides:[4],requiredNativeChartOwnerSlides:[5,6],materializeLiteralChartWorkbooks:true,fontPolicy:{basis:'design',families:[FONT]},verifyArtifactToolImport:true,receiptPath:receipt});
await fs.copyFile(validated,path.join(ROOT,'presentation/draft_presentation.pptx'));
await fs.copyFile(receipt,path.join(BUILD,'validation.json'));
for (const [i,s] of p.slides.items.entries()) {
  const blob=await p.export({slide:s,format:'png',scale:1});
  await fs.writeFile(path.join(BUILD,'previews',`slide-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()));
}
try {
  const pdf=await p.export({format:'pdf'});
  await fs.writeFile(path.join(ROOT,'presentation/draft_presentation.pdf'),new Uint8Array(await pdf.arrayBuffer()));
} catch (error) {
  const converter=path.join(process.env.CODEX_PRIMARY_RUNTIME_ROOT,'dependencies/bin/override/soffice');
  execFileSync(converter,['--headless',`-env:UserInstallation=${pathToFileURL(path.join(BUILD,'lo-profile')).href}`,'--convert-to','pdf','--outdir',path.join(ROOT,'presentation'),path.join(ROOT,'presentation/draft_presentation.pptx')],{stdio:'inherit'});
}
console.log(JSON.stringify({slides:p.slides.items.length,pptx:'presentation/draft_presentation.pptx',pdf:'presentation/draft_presentation.pdf'}));
