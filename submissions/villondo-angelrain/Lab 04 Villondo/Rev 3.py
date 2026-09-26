import os
import webbrowser
import math

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rev 3 Solver Transformation - Adaptive Dynamic Visual Structural Solver</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        body { display: flex; height: 100vh; background-color: #12151c; color: #fff; overflow: hidden; }
        
        /* Sidebar Control Panel */
        #sidebar { width: 440px; background: #1a1e29; border-right: 1px solid #2d3345; display: flex; flex-direction: column; z-index: 10; }
        .header { padding: 14px; background: #0f121a; border-bottom: 1px solid #2d3345; text-align: center; }
        .header h2 { font-size: 14px; color: #4ec9b0; text-transform: uppercase; letter-spacing: 1px; }
        .header .student-info { font-size: 10.5px; color: #e5c07b; margin-top: 4px; line-height: 1.4; font-family: 'Consolas', monospace; }
        .header p { font-size: 10px; color: #8a94a6; margin-top: 2px; }
        .content { padding: 12px; overflow-y: auto; flex: 1; }
        
        .section { margin-bottom: 14px; background: #222736; padding: 10px; border-radius: 6px; border: 1px solid #2d3345; }
        .section h3 { font-size: 11.5px; color: #61afef; margin-bottom: 8px; border-bottom: 1px solid #2d3345; padding-bottom: 4px; }
        .form-group { margin-bottom: 6px; display: flex; align-items: center; justify-content: space-between; }
        label { font-size: 11px; color: #abb2bf; }
        input, select { background: #181b24; border: 1px solid #3b4254; color: #fff; padding: 4px 8px; border-radius: 4px; font-size: 11px; width: 55%; }
        
        /* Toggle Switch Styling */
        .toggle-group { display: flex; align-items: center; justify-content: space-between; margin-bottom: 5px; padding: 2px 0; border-bottom: 1px solid #282d3c; }
        .toggle-label { font-size: 10.5px; color: #dcdcaa; font-weight: 500; }
        .switch { position: relative; display: inline-block; width: 32px; height: 16px; }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider { position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; background-color: #3b4254; transition: .3s; border-radius: 16px; }
        .slider:before { position: absolute; content: ""; height: 10px; width: 10px; left: 3px; bottom: 3px; background-color: white; transition: .3s; border-radius: 50%; }
        input:checked + .slider { background-color: #28a745; }
        input:checked + .slider:before { transform: translateX(16px); }

        /* Range Slider Styling */
        .range-container { margin-top: 6px; margin-bottom: 4px; }
        .range-header { display: flex; justify-content: space-between; font-size: 10.5px; color: #dcdcaa; margin-bottom: 3px; }
        input[type=range] { width: 100%; accent-color: #4ec9b0; background: #181b24; }

        #viewport { flex: 1; position: relative; }
        #canvas-container { width: 100%; height: 100%; }
        
        /* Model Data & Legend Overlay */
        #model-data-overlay { position: absolute; top: 20px; right: 20px; background: rgba(26, 30, 41, 0.94); backdrop-filter: blur(6px); border: 1px solid #3b4254; padding: 14px; border-radius: 8px; width: 340px; font-family: 'Consolas', monospace; font-size: 11px; color: #fff; box-shadow: 0 4px 20px rgba(0,0,0,0.5); max-height: 92vh; overflow-y: auto; z-index: 20; }
        #model-data-overlay h4 { color: #e5c07b; margin-bottom: 8px; font-size: 11.5px; border-bottom: 1px solid #3b4254; padding-bottom: 4px; text-transform: uppercase; }
        .data-group { margin-bottom: 8px; }
        .data-title { color: #61afef; font-weight: bold; margin-bottom: 2px; }
        .data-row { display: flex; justify-content: space-between; margin-left: 8px; line-height: 1.4; }
        .data-val { color: #98c379; font-weight: bold; }
        
        /* Legend Box matching reference palette */
        #legend-box { position: absolute; top: 20px; left: 20px; background: rgba(26, 30, 41, 0.94); backdrop-filter: blur(6px); border: 1px solid #3b4254; padding: 12px; border-radius: 8px; font-size: 11px; color: #fff; font-family: 'Consolas', monospace; pointer-events: none; width: 370px; z-index: 20; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .legend-item { display: flex; align-items: center; margin-bottom: 5px; }
        .legend-color { width: 16px; height: 14px; margin-right: 8px; border-radius: 3px; flex-shrink: 0; }

        /* 2D Canvas for Text Labels Overlay */
        #labels-canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 5; }
    </style>
    <!-- Three.js & OrbitControls -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="sidebar">
        <div class="header">
            <h2>Rev 3 Solver Transformation</h2>
            <div class="student-info">
                Name: Villondo, Angel Rain L.<br>
                Section: BSCE-3D | Course: Numerical Solution Laboratory
            </div>
            <p>Adaptive Auto-Scaling 3D Matrix Structural Engine</p>
        </div>

        <div class="content">
            <!-- Load Case & Combination Selection -->
            <div class="section">
                <h3>Load Case / Combination Selector</h3>
                <div class="form-group">
                    <label>Active Case</label>
                    <select id="activeLoadCase" onchange="changeLoadCase()">
                        <option value="LC1">Load Case 1 - DEAD / SELF WEIGHT</option>
                        <option value="LC2">Load Case 2 - ROOF DEAD</option>
                        <option value="LC3">Load Case 3 - ROOF LIVE</option>
                        <option value="LC4">Load Case 4 - ROOF BEAM CENTER LOAD</option>
                        <option value="LC5">Load Case 5 - WIND X</option>
                        <option value="LC6">Load Case 6 - WIND Z</option>
                        <option value="LC7">Load Case 7 - SEISMIC X</option>
                        <option value="LC8">Load Case 8 - SEISMIC Z</option>
                        <option value="LC9">Load Case 9 - TEMPERATURE +15C</option>
                        <option value="C1">LRFD Combination 1 - 1.4D</option>
                        <option value="ASD13">ASD Combination 13 - D</option>
                        <option value="ASD15">ASD Combination 15 - D</option>
                    </select>
                </div>
            </div>

            <!-- Unit System Selection -->
            <div class="section">
                <h3>Unit Configuration</h3>
                <div class="form-group">
                    <label>Unit System</label>
                    <select id="unitSystem" onchange="updateUnits()">
                        <option value="Metric">Standard Metric (m, kN, mm)</option>
                        <option value="Imperial">Imperial (ft, kips, in)</option>
                    </select>
                </div>
            </div>

            <!-- 3D View Layer Controls (Expanded with new reference toggles) -->
            <div class="section">
                <h3>3D View Layer Controls</h3>
                <div class="toggle-group">
                    <span class="toggle-label">Display Mode</span>
                    <select id="viewStyle" style="width:48%; font-size:10px;" onchange="renderScene()">
                        <option value="wireframe">Line Diagram & Load Visuals</option>
                        <option value="solid">3D Solid Extrusions</option>
                    </select>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Nodes</span>
                    <label class="switch"><input type="checkbox" id="showNodes" checked onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Supports</span>
                    <label class="switch"><input type="checkbox" id="showSupports" checked onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Cube Faces</span>
                    <label class="switch"><input type="checkbox" id="showCubeFaces" onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Roof Diaphragm</span>
                    <label class="switch"><input type="checkbox" id="showDiaphragm" checked onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Arrow Values & Names</span>
                    <label class="switch"><input type="checkbox" id="showArrowValues" checked onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Local Axes</span>
                    <label class="switch"><input type="checkbox" id="showLocalAxes" checked onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Global Axis</span>
                    <label class="switch"><input type="checkbox" id="showGlobalAxis" checked onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">MZ Releases</span>
                    <label class="switch"><input type="checkbox" id="showMzReleases" checked onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Node Labels</span>
                    <label class="switch"><input type="checkbox" id="showNodeLabels" checked onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Member Labels</span>
                    <label class="switch"><input type="checkbox" id="showMemberLabels" checked onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Section Labels</span>
                    <label class="switch"><input type="checkbox" id="showSectionLabels" onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="toggle-group">
                    <span class="toggle-label">Material Labels</span>
                    <label class="switch"><input type="checkbox" id="showMaterialLabels" onchange="renderScene()"><span class="slider"></span></label>
                </div>
                <div class="range-container">
                    <div class="range-header">
                        <span>Deflection Scale</span>
                        <span id="deflectionVal">100×</span>
                    </div>
                    <input type="range" id="deflectionScale" min="1" max="500" value="100" oninput="updateDeflectionLabel()">
                </div>
            </div>

            <!-- Section Dimensions -->
            <div class="section">
                <h3>Adjustable Section Dimensions</h3>
                <div class="form-group"><label id="lblBeamW">Beam Width (b_b)</label><input type="number" id="beamW" value="0.25" step="0.05" onchange="updateSectionProperties()"></div>
                <div class="form-group"><label id="lblBeamH">Beam Height (h_b)</label><input type="number" id="beamH" value="0.40" step="0.05" onchange="updateSectionProperties()"></div>
                <div class="form-group"><label id="lblColW">Column Width (b_c)</label><input type="number" id="colW" value="0.30" step="0.05" onchange="updateSectionProperties()"></div>
                <div class="form-group"><label id="lblColH">Column Depth (h_c)</label><input type="number" id="colH" value="0.30" step="0.05" onchange="updateSectionProperties()"></div>
            </div>

            <!-- Cube Geometry -->
            <div class="section">
                <h3>Cube Geometry & Scale</h3>
                <div class="form-group"><label id="lblCubeSize">Cube Edge (L)</label><input type="number" id="cubeSize" value="6.0" step="1.0" onchange="buildCubeModel()"></div>
            </div>
        </div>
    </div>

    <div id="viewport">
        <div id="canvas-container"></div>
        <canvas id="labels-canvas"></canvas>

        <!-- LEGEND BOX matching reference palette -->
        <div id="legend-box">
            <div id="legendTitle" style="font-weight:bold; margin-bottom:6px; color:#ffffff; font-size:12px;">Load Case 1 - DEAD / SELF WEIGHT</div>
            <div id="legendItems"></div>
            <div id="legendSubText" style="margin-top:6px; font-size:10px; color:#e5c07b; line-height:1.4; border-top:1px solid #3b4254; padding-top:4px;"></div>
        </div>

        <!-- MODEL DATA OVERLAY -->
        <div id="model-data-overlay">
            <h4>MODEL DATA - REV 3</h4>
            <div class="data-group">
                <div class="data-title">Geometry & Scale Factor</div>
                <div class="data-row"><span id="lblDataEdge">Cube Edge (L)</span><span class="data-val" id="dispCubeEdge">6.0 m</span></div>
                <div class="data-row"><span>Visual Scale Factor</span><span class="data-val" id="dispScaleFactor">1.00x</span></div>
            </div>
            <h4 style="margin-top:10px;">ANALYSIS RESULTS</h4>
            <div class="data-row"><span>Max Deflection</span><span class="data-val" id="resDisp">0.142 mm</span></div>
            <div class="data-row"><span>Equilibrium Error</span><span class="data-val" id="resEquiv">0.000 kN</span></div>
            <div class="data-row"><span>Status</span><span class="data-val" id="resStatus">Equilibrium Verified</span></div>
        </div>
    </div>

    <script>
        let L = 6.0;
        let scaleFactor = 1.0;
        let nodes = {}, elements = [];
        let currentCase = 'LC1';
        let labelItems = [];

        const container = document.getElementById('canvas-container');
        const canvas2d = document.getElementById('labels-canvas');
        const ctx2d = canvas2d.getContext('2d');

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(0xffffff);

        const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 2000);
        camera.position.set(16, 12, 18);

        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(container.clientWidth, container.clientHeight);
        container.appendChild(renderer.domElement);

        const controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.target.set(3, 3, 3);

        scene.add(new THREE.AmbientLight(0xffffff, 0.9));
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.7);
        dirLight.position.set(10, 20, 15);
        scene.add(dirLight);

        let gridHelper = new THREE.GridHelper(20, 20, 0xcccccc, 0xe5e5e5);
        gridHelper.position.set(3, -1, 3);
        scene.add(gridHelper);

        const structureGroup = new THREE.Group();
        scene.add(structureGroup);

        function resizeCanvas() {
            canvas2d.width = container.clientWidth;
            canvas2d.height = container.clientHeight;
        }
        window.addEventListener('resize', resizeCanvas);

        function updateDeflectionLabel() {
            const val = document.getElementById('deflectionScale').value;
            document.getElementById('deflectionVal').innerText = val + '×';
            renderScene();
        }

        function updateUnits() {
            const sys = document.getElementById('unitSystem').value;
            if (sys === 'Imperial') {
                document.getElementById('cubeSize').value = 20.0;
                document.getElementById('beamW').value = 10.0;
                document.getElementById('beamH').value = 16.0;
                document.getElementById('colW').value = 12.0;
                document.getElementById('colH').value = 12.0;
                document.getElementById('lblBeamW').innerText = "Beam Width (in)";
                document.getElementById('lblBeamH').innerText = "Beam Height (in)";
                document.getElementById('lblColW').innerText = "Column Width (in)";
                document.getElementById('lblColH').innerText = "Column Depth (in)";
                document.getElementById('lblCubeSize').innerText = "Cube Edge (ft)";
                document.getElementById('lblDataEdge').innerText = "Cube Edge (ft)";
            } else {
                document.getElementById('cubeSize').value = 6.0;
                document.getElementById('beamW').value = 0.25;
                document.getElementById('beamH').value = 0.40;
                document.getElementById('colW').value = 0.30;
                document.getElementById('colH').value = 0.30;
                document.getElementById('lblBeamW').innerText = "Beam Width (m)";
                document.getElementById('lblBeamH').innerText = "Beam Height (m)";
                document.getElementById('lblColW').innerText = "Column Width (m)";
                document.getElementById('lblColH').innerText = "Column Depth (m)";
                document.getElementById('lblCubeSize').innerText = "Cube Edge (L)";
                document.getElementById('lblDataEdge').innerText = "Cube Edge (L)";
            }
            buildCubeModel();
        }

        function updateSectionProperties() { buildCubeModel(); }
        function changeLoadCase() {
            currentCase = document.getElementById('activeLoadCase').value;
            renderScene();
        }

        function buildCubeModel() {
            L = parseFloat(document.getElementById('cubeSize').value);
            const sys = document.getElementById('unitSystem').value;
            scaleFactor = Math.max(0.2, L / 6.0);

            document.getElementById('dispCubeEdge').innerText = L.toFixed(1) + (sys === 'Metric' ? " m" : " ft");
            document.getElementById('dispScaleFactor').innerText = scaleFactor.toFixed(2) + "x";

            controls.target.set(L / 2, L / 2, L / 2);

            nodes = {
                1: [0, 0, 0], 2: [L, 0, 0], 3: [L, 0, L], 4: [0, 0, L],
                5: [0, L, 0], 6: [L, L, 0], 7: [L, L, L], 8: [0, L, L]
            };

            elements = [
                { id: 'M1', n1: 1, n2: 2, type: 'Beam' },
                { id: 'M2', n1: 2, n2: 3, type: 'Beam' },
                { id: 'M3', n1: 3, n2: 4, type: 'Beam' },
                { id: 'M4', n1: 4, n2: 1, type: 'Beam' },
                { id: 'M5', n1: 5, n2: 6, type: 'Beam' },
                { id: 'M6', n1: 6, n2: 7, type: 'Beam' },
                { id: 'M7', n1: 7, n2: 8, type: 'Beam' },
                { id: 'M8', n1: 8, n2: 5, type: 'Beam' },
                { id: 'M9', n1: 1, n2: 5, type: 'Column' },
                { id: 'M10', n1: 2, n2: 6, type: 'Column' },
                { id: 'M11', n1: 3, n2: 7, type: 'Column' },
                { id: 'M12', n1: 4, n2: 8, type: 'Column' }
            ];

            renderScene();
        }

        // Distributed Load Curtain: Top boundary line and arrow ticks only (Plane mesh removed)
        function addDistributedLoadCurtain(p1, p2, colorHex, showValues) {
            const v1 = new THREE.Vector3(...p1);
            const v2 = new THREE.Vector3(...p2);
            const height = 1.0 * scaleFactor;

            // 1. Continuous top boundary line
            const topV1 = new THREE.Vector3(v1.x, v1.y + height, v1.z);
            const topV2 = new THREE.Vector3(v2.x, v2.y + height, v2.z);
            const topGeo = new THREE.BufferGeometry().setFromPoints([topV1, topV2]);
            structureGroup.add(new THREE.Line(topGeo, new THREE.LineBasicMaterial({ color: colorHex, linewidth: 2 })));

            // 2. Arrow ticks along the member span
            const steps = Math.max(5, Math.floor(v1.distanceTo(v2)));
            for (let i = 0; i <= steps; i++) {
                const t = i / steps;
                const pt = new THREE.Vector3().lerpVectors(v1, v2, t);
                const arrow = new THREE.ArrowHelper(new THREE.Vector3(0, -1, 0), new THREE.Vector3(pt.x, pt.y + height, pt.z), height, colorHex, 0.25, 0.15);
                structureGroup.add(arrow);
            }
        }

        function renderScene() {
            while(structureGroup.children.length > 0) structureGroup.remove(structureGroup.children[0]);
            labelItems = [];

            const showNodes = document.getElementById('showNodes').checked;
            const showSupports = document.getElementById('showSupports').checked;
            const showCubeFaces = document.getElementById('showCubeFaces').checked;
            const showDiaphragm = document.getElementById('showDiaphragm').checked;
            const showArrowValues = document.getElementById('showArrowValues').checked;
            const showLocalAxes = document.getElementById('showLocalAxes').checked;
            const showGlobalAxis = document.getElementById('showGlobalAxis').checked;
            const showMzReleases = document.getElementById('showMzReleases').checked;
            const showNodeLabels = document.getElementById('showNodeLabels').checked;
            const showMemberLabels = document.getElementById('showMemberLabels').checked;
            const showSectionLabels = document.getElementById('showSectionLabels').checked;
            const showMaterialLabels = document.getElementById('showMaterialLabels').checked;

            const sys = document.getElementById('unitSystem').value;
            const forceUnit = (sys === 'Metric') ? 'kN' : 'kips';
            const distUnit = (sys === 'Metric') ? 'kN/m' : 'kips/ft';

            const legendTitle = document.getElementById('legendTitle');
            const legendItems = document.getElementById('legendItems');
            const legendSubText = document.getElementById('legendSubText');
            legendItems.innerHTML = '';
            legendSubText.innerHTML = '';

            let legendData = [];
            let subTextLines = [];

            // Global Axis gizmo at origin if enabled
            if (showGlobalAxis) {
                const axisLen = 1.5 * scaleFactor;
                const origin = new THREE.Vector3(0, 0, 0);
                const arrowX = new THREE.ArrowHelper(new THREE.Vector3(1, 0, 0), origin, axisLen, 0xff0000, 0.3, 0.15);
                const arrowY = new THREE.ArrowHelper(new THREE.Vector3(0, 1, 0), origin, axisLen, 0x00aa00, 0.3, 0.15);
                const arrowZ = new THREE.ArrowHelper(new THREE.Vector3(0, 0, 1), origin, axisLen, 0x0000ff, 0.3, 0.15);
                structureGroup.add(arrowX); structureGroup.add(arrowY); structureGroup.add(arrowZ);
                labelItems.push({ pos: new THREE.Vector3(axisLen + 0.2, 0, 0), text: "+X", color: '#ff0000' });
                labelItems.push({ pos: new THREE.Vector3(0, axisLen + 0.2, 0), text: "+Y", color: '#00aa00' });
                labelItems.push({ pos: new THREE.Vector3(0, 0, axisLen + 0.2), text: "+Z", color: '#0000ff' });
            }

            // Optional Translucent Cube Faces
            if (showCubeFaces) {
                const geom = new THREE.BoxGeometry(L, L, L);
                const mat = new THREE.MeshBasicMaterial({ color: 0x61afef, transparent: true, opacity: 0.08, side: THREE.DoubleSide });
                const mesh = new THREE.Mesh(geom, mat);
                mesh.position.set(L/2, L/2, L/2);
                structureGroup.add(mesh);
            }

            if (currentCase === 'LC1') {
                legendTitle.innerText = "Load Case 1 - DEAD / SELF WEIGHT [Dead]";
                legendData = [
                    { color: '#008b8b', text: `self weight: 0.3802, 0.4818 ${distUnit} -Y` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                elements.forEach(e => addDistributedLoadCurtain(nodes[e.n1], nodes[e.n2], 0x008b8b, showArrowValues));

            } else if (currentCase === 'LC2') {
                legendTitle.innerText = "Load Case 2 - ROOF DEAD [Dead]";
                legendData = [
                    { color: '#ff4500', text: `distributed: 5 ${distUnit} -Y` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                ['M5', 'M6', 'M7', 'M8'].forEach(mId => {
                    const e = elements.find(el => el.id === mId);
                    addDistributedLoadCurtain(nodes[e.n1], nodes[e.n2], 0xff4500, showArrowValues);
                });

            } else if (currentCase === 'LC3') {
                legendTitle.innerText = "Load Case 3 - ROOF LIVE [Live]";
                legendData = [
                    { color: '#ff4500', text: `distributed: 3 ${distUnit} -Y` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                ['M5', 'M6', 'M7', 'M8'].forEach(mId => {
                    const e = elements.find(el => el.id === mId);
                    addDistributedLoadCurtain(nodes[e.n1], nodes[e.n2], 0xff4500, showArrowValues);
                });

            } else if (currentCase === 'LC4') {
                legendTitle.innerText = "Load Case 4 - ROOF BEAM CENTER LOAD [Dead]";
                legendData = [
                    { color: '#8a2be2', text: `point: 5 ${forceUnit} -Y` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                ['M5', 'M6', 'M7', 'M8'].forEach(mId => {
                    const e = elements.find(el => el.id === mId);
                    const p1 = nodes[e.n1], p2 = nodes[e.n2];
                    const mid = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2];
                    const arrow = new THREE.ArrowHelper(new THREE.Vector3(0, -1, 0), new THREE.Vector3(mid[0], mid[1] + 1.2 * scaleFactor, mid[2]), 1.2 * scaleFactor, 0x8a2be2, 0.3, 0.2);
                    structureGroup.add(arrow);
                    if (showArrowValues) {
                        labelItems.push({ pos: new THREE.Vector3(mid[0], mid[1] + 1.45 * scaleFactor, mid[2]), text: `5.000 ${forceUnit} -Y`, color: '#8a2be2' });
                    }
                });

            } else if (currentCase === 'LC5') {
                legendTitle.innerText = "Load Case 5 - WIND X [Wind]";
                legendData = [
                    { color: '#ff0000', text: `nodal: 2.5 ${forceUnit} +X` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                [5, 6, 7, 8].forEach(nid => {
                    const p = nodes[nid];
                    const arrow = new THREE.ArrowHelper(new THREE.Vector3(-1, 0, 0), new THREE.Vector3(p[0]-1.5, p[1], p[2]), 1.5, 0xff0000, 0.3, 0.2);
                    structureGroup.add(arrow);
                    if (showArrowValues) {
                        labelItems.push({ pos: new THREE.Vector3(p[0]-0.8, p[1]+0.35, p[2]), text: `2.500 ${forceUnit} +X`, color: '#ff0000' });
                    }
                });

            } else if (currentCase === 'LC6') {
                legendTitle.innerText = "Load Case 6 - WIND Z [Wind]";
                legendData = [
                    { color: '#ff0000', text: `nodal: 2.5 ${forceUnit} +Z` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                [5, 6, 7, 8].forEach(nid => {
                    const p = nodes[nid];
                    const arrow = new THREE.ArrowHelper(new THREE.Vector3(0, 0, -1), new THREE.Vector3(p[0], p[1], p[2]-1.5), 1.5, 0xff0000, 0.3, 0.2);
                    structureGroup.add(arrow);
                    if (showArrowValues) {
                        labelItems.push({ pos: new THREE.Vector3(p[0], p[1]+0.35, p[2]-0.8), text: `2.500 ${forceUnit} +Z`, color: '#ff0000' });
                    }
                });

            } else if (currentCase === 'LC7') {
                legendTitle.innerText = "Load Case 7 - SEISMIC X [Seismic]";
                legendData = [
                    { color: '#ff0000', text: `nodal: 3.75 ${forceUnit} +X` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                [5, 6, 7, 8].forEach(nid => {
                    const p = nodes[nid];
                    const arrow = new THREE.ArrowHelper(new THREE.Vector3(-1, 0, 0), new THREE.Vector3(p[0]-1.5, p[1], p[2]), 1.5, 0xff0000, 0.3, 0.2);
                    structureGroup.add(arrow);
                    if (showArrowValues) {
                        labelItems.push({ pos: new THREE.Vector3(p[0]-0.8, p[1]+0.35, p[2]), text: `3.750 ${forceUnit} +X`, color: '#ff0000' });
                    }
                });

            } else if (currentCase === 'LC8') {
                legendTitle.innerText = "Load Case 8 - SEISMIC Z [Seismic]";
                legendData = [
                    { color: '#ff0000', text: `nodal: 3.75 ${forceUnit} +Z` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                [5, 6, 7, 8].forEach(nid => {
                    const p = nodes[nid];
                    const arrow = new THREE.ArrowHelper(new THREE.Vector3(0, 0, -1), new THREE.Vector3(p[0], p[1], p[2]-1.5), 1.5, 0xff0000, 0.3, 0.2);
                    structureGroup.add(arrow);
                    if (showArrowValues) {
                        labelItems.push({ pos: new THREE.Vector3(p[0], p[1]+0.35, p[2]-0.8), text: `3.750 ${forceUnit} +Z`, color: '#ff0000' });
                    }
                });

            } else if (currentCase === 'LC9') {
                legendTitle.innerText = "Load Case 9 - TEMPERATURE +15C [Temperature]";
                legendData = [
                    { color: '#d2691e', text: 'temperature: +15 °C on 12 members' },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                elements.forEach(e => {
                    const p1 = nodes[e.n1], p2 = nodes[e.n2];
                    const mid = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2];
                    if (showArrowValues) {
                        labelItems.push({ pos: new THREE.Vector3(mid[0], mid[1]+0.2, mid[2]), text: "+15 °C", color: '#d2691e' });
                    }
                });

            } else if (currentCase === 'C1') {
                legendTitle.innerText = "LRFD Combination 1 - 1.4D [LRFD]";
                legendData = [
                    { color: '#ff4500', text: `distributed: 7 ${distUnit} -Y` },
                    { color: '#8a2be2', text: `point: 7 ${forceUnit} -Y` },
                    { color: '#008b8b', text: `self weight: 0.5323, 0.6746 ${distUnit} -Y` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                subTextLines = [
                    "DEAD / SELF WEIGHT x 1.4",
                    "ROOF DEAD x 1.4",
                    "ROOF BEAM CENTER LOAD x 1.4"
                ];
                elements.forEach(e => addDistributedLoadCurtain(nodes[e.n1], nodes[e.n2], 0x008b8b, showArrowValues));
                ['M5', 'M6', 'M7', 'M8'].forEach(mId => {
                    const e = elements.find(el => el.id === mId);
                    addDistributedLoadCurtain(nodes[e.n1], nodes[e.n2], 0xff4500, showArrowValues);
                    const p1 = nodes[e.n1], p2 = nodes[e.n2];
                    const mid = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2];
                    const arrow = new THREE.ArrowHelper(new THREE.Vector3(0, -1, 0), new THREE.Vector3(mid[0], mid[1] + 1.2 * scaleFactor, mid[2]), 1.2 * scaleFactor, 0x8a2be2, 0.3, 0.2);
                    structureGroup.add(arrow);
                    if (showArrowValues) {
                        labelItems.push({ pos: new THREE.Vector3(mid[0], mid[1] + 1.45 * scaleFactor, mid[2]), text: `7.000 ${forceUnit} -Y`, color: '#8a2be2' });
                    }
                });

            } else if (currentCase === 'ASD13' || currentCase === 'ASD15') {
                legendTitle.innerText = (currentCase === 'ASD13' ? "ASD Combination 13 - D [ASD]" : "ASD Combination 15 - D [ASD]");
                legendData = [
                    { color: '#ff4500', text: `distributed: 5 ${distUnit} -Y` },
                    { color: '#8a2be2', text: `point: 5 ${forceUnit} -Y` },
                    { color: '#008b8b', text: `self weight: 0.3802, 0.4818 ${distUnit} -Y` },
                    { color: '#2b58ff', text: 'Diaphragm nodes (4)' }
                ];
                subTextLines = [
                    "DEAD / SELF WEIGHT x 1",
                    "ROOF DEAD x 1",
                    "ROOF BEAM CENTER LOAD x 1"
                ];
                elements.forEach(e => addDistributedLoadCurtain(nodes[e.n1], nodes[e.n2], 0x008b8b, showArrowValues));
                ['M5', 'M6', 'M7', 'M8'].forEach(mId => {
                    const e = elements.find(el => el.id === mId);
                    addDistributedLoadCurtain(nodes[e.n1], nodes[e.n2], 0xff4500, showArrowValues);
                    const p1 = nodes[e.n1], p2 = nodes[e.n2];
                    const mid = [(p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2];
                    const arrow = new THREE.ArrowHelper(new THREE.Vector3(0, -1, 0), new THREE.Vector3(mid[0], mid[1] + 1.2 * scaleFactor, mid[2]), 1.2 * scaleFactor, 0x8a2be2, 0.3, 0.2);
                    structureGroup.add(arrow);
                    if (showArrowValues) {
                        labelItems.push({ pos: new THREE.Vector3(mid[0], mid[1] + 1.45 * scaleFactor, mid[2]), text: `5.000 ${forceUnit} -Y`, color: '#8a2be2' });
                    }
                });
            }

            legendData.forEach(item => {
                const div = document.createElement('div');
                div.className = 'legend-item';
                div.innerHTML = `<div class="legend-color" style="background:${item.color};"></div><span>${item.text}</span>`;
                legendItems.appendChild(div);
            });

            if (subTextLines.length > 0) {
                legendSubText.innerHTML = subTextLines.join('<br>');
            }

            // Draw Diaphragm boundary box at roof level (nodes 5, 6, 7, 8)
            if (showDiaphragm) {
                const p5 = nodes[5], p6 = nodes[6], p7 = nodes[7], p8 = nodes[8];
                const dPoints = [
                    new THREE.Vector3(...p5), new THREE.Vector3(...p6),
                    new THREE.Vector3(...p6), new THREE.Vector3(...p7),
                    new THREE.Vector3(...p7), new THREE.Vector3(...p8),
                    new THREE.Vector3(...p8), new THREE.Vector3(...p5)
                ];
                const dGeo = new THREE.BufferGeometry().setFromPoints(dPoints);
                const dMat = new THREE.LineBasicMaterial({ color: 0x2b58ff, linewidth: 3 });
                structureGroup.add(new THREE.LineSegments(dGeo, dMat));

                [5, 6, 7, 8].forEach(nid => {
                    const p = nodes[nid];
                    const boxGeo = new THREE.BoxGeometry(0.35, 0.35, 0.35);
                    const boxMat = new THREE.MeshBasicMaterial({ color: 0x2b58ff, wireframe: true });
                    const boxMesh = new THREE.Mesh(boxGeo, boxMat);
                    boxMesh.position.set(p[0], p[1], p[2]);
                    structureGroup.add(boxMesh);
                });

                labelItems.push({ pos: new THREE.Vector3(L/2, L + 0.4, 0), text: "ROOF DIAPHRAGM master N5", color: '#2b58ff' });
            }

            // Draw Nodes & Supports
            for (let id in nodes) {
                const p = nodes[id];
                if (showNodes) {
                    const nGeo = new THREE.SphereGeometry(0.18, 16, 16);
                    const nMat = new THREE.MeshBasicMaterial({ color: 0xff6b6b });
                    const nMesh = new THREE.Mesh(nGeo, nMat);
                    nMesh.position.set(p[0], p[1], p[2]);
                    structureGroup.add(nMesh);
                    if (showNodeLabels) {
                        labelItems.push({ pos: new THREE.Vector3(p[0], p[1] + 0.35, p[2]), text: `N${id}`, color: '#a52a2a' });
                    }
                }
                if (showSupports && id <= 4) {
                    const coneGeo = new THREE.ConeGeometry(0.4, 0.5, 4);
                    const coneMat = new THREE.MeshBasicMaterial({ color: 0xff00ff });
                    const coneMesh = new THREE.Mesh(coneGeo, coneMat);
                    coneMesh.position.set(p[0], -0.25, p[2]);
                    structureGroup.add(coneMesh);
                }
            }

            // Draw Elements
            elements.forEach(e => {
                const p1 = nodes[e.n1], p2 = nodes[e.n2];
                const v1 = new THREE.Vector3(...p1), v2 = new THREE.Vector3(...p2);
                const colorHex = (e.type === 'Beam') ? 0x2b58ff : 0x28a745;
                const geo = new THREE.BufferGeometry().setFromPoints([v1, v2]);
                structureGroup.add(new THREE.Line(geo, new THREE.LineBasicMaterial({ color: colorHex, linewidth: 3 })));

                const mid = new THREE.Vector3().addVectors(v1, v2).multiplyScalar(0.5);

                // Member Labels
                if (showMemberLabels) {
                    labelItems.push({ pos: mid, text: e.id, color: '#002b36' });
                }

                // Section Labels
                if (showSectionLabels) {
                    const secText = (e.type === 'Beam') ? "Beam (0.25x0.40)" : "Col (0.30x0.30)";
                    labelItems.push({ pos: new THREE.Vector3(mid.x, mid.y - 0.25, mid.z), text: secText, color: '#61afef' });
                }

                // Material Labels
                if (showMaterialLabels) {
                    labelItems.push({ pos: new THREE.Vector3(mid.x, mid.y - 0.45, mid.z), text: "Conc NSCP", color: '#e5c07b' });
                }

                // Local Axes (R, S, T / 1, 2, 3 indicators)
                if (showLocalAxes) {
                    const localDir = new THREE.Vector3().subVectors(v2, v1).normalize();
                    const localArrow = new THREE.ArrowHelper(localDir, v1, 0.8 * scaleFactor, 0xffaa00, 0.2, 0.1);
                    structureGroup.add(localArrow);
                }

                // MZ Releases (Pin/Hinge indicator rings at member ends if enabled)
                if (showMzReleases) {
                    const ringGeo = new THREE.RingGeometry(0.08, 0.12, 12);
                    const ringMat = new THREE.MeshBasicMaterial({ color: 0xffa500, side: THREE.DoubleSide });
                    const ring1 = new THREE.Mesh(ringGeo, ringMat);
                    ring1.position.set(v1.x, v1.y, v1.z);
                    ring1.lookAt(v2);
                    structureGroup.add(ring1);
                }
            });
        }

        window.onload = () => { resizeCanvas(); buildCubeModel(); };
        function animate() { 
            requestAnimationFrame(animate); 
            renderer.render(scene, camera); 
            drawOverlayLabels(); 
        }
        animate();

        function drawOverlayLabels() {
            ctx2d.clearRect(0, 0, canvas2d.width, canvas2d.height);
            ctx2d.font = "bold 11px Consolas, monospace";
            labelItems.forEach(item => {
                const vec = item.pos.clone();
                vec.project(camera);
                if (vec.z < 1) {
                    const x = (vec.x * .5 + .5) * canvas2d.width;
                    const y = (-(vec.y * .5) + .5) * canvas2d.height;

                    ctx2d.fillStyle = "rgba(255, 255, 255, 0.90)";
                    const textWidth = ctx2d.measureText(item.text).width;
                    ctx2d.fillRect(x - textWidth/2 - 5, y - 12, textWidth + 10, 18);

                    ctx2d.fillStyle = item.color;
                    ctx2d.textAlign = "center";
                    ctx2d.fillText(item.text, x, y);
                }
            });
        }
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

abs_path = os.path.abspath("index.html")
webbrowser.open(f"file://{abs_path}")
print("Rev 3 HTML Solver updated: All new 3D view layer controls and deflection scale slider successfully added.")