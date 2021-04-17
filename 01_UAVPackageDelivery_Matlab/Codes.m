% At uavScenarioBlock.m file:
% 'stepImpl' function has been modified to the code below in order to allow the
% visualization of the UAV's path in the block scenario model during the simulation.

        function pts = stepImpl(obj, position, orientation)
            % return point cloud based on input pose
            
            obj.Scenario.advance();
            show3D(obj.Scenario)
            view([0 90])
            grid on;
            axis([-150 52 -250 20])
            hold on;
            %text(0, -180, ['Current Sim.Time: ' string(obj.Scenario.CurrentTime)])
            obj.Platform.move([position, zeros(1,6), eul2quat(orientation), zeros(1,3)]);
            obj.Scenario.updateSensors();
            [~, ~, ptCloud] = obj.Lidar.read();
            pts = ptCloud.Location;
            pts(:, 1:size(pts,2),:) = pts(:,size(pts,2):-1:1,:);
        end