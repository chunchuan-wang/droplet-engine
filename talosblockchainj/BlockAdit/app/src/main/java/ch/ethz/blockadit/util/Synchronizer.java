package ch.ethz.blockadit.util;

import android.content.Context;

import java.util.Date;

import ch.ethz.blockadit.blockadit.TalosAPIFactory;
import ch.ethz.blockadit.blockadit.BlockAditFitbitAPI;
import ch.ethz.blockadit.fitbitapi.FitbitAPI;
import ch.ethz.blockadit.fitbitapi.FitbitAPIException;
import ch.ethz.blockadit.fitbitapi.TokenInfo;
import ch.ethz.blockadit.fitbitapi.model.CaloriesQuery;
import ch.ethz.blockadit.fitbitapi.model.DistQuery;
import ch.ethz.blockadit.fitbitapi.model.FloorQuery;
import ch.ethz.blockadit.fitbitapi.model.HeartQuery;
import ch.ethz.blockadit.fitbitapi.model.StepsQuery;


/*
 * Copyright (c) 2016, Institute for Pervasive Computing, ETH Zurich.
 * All rights reserved.
 *
 * Author:
 *       Lukas Burkhalter <lubu@student.ethz.ch>
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * 3. Neither the name of the copyright holder nor the names of its
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
 * COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 */

public class Synchronizer {

    private BlockAditFitbitAPI talosApi;

    private FitbitAPI fitbit;

    public Synchronizer(Context con, TokenInfo token) {
        talosApi = TalosAPIFactory.createAPI(con);
        fitbit = new FitbitAPI(token);
    }

    public void transferDataStepFromDate(DemoUser u, Date date) throws TalosModuleException, FitbitAPIException {
        StepsQuery query = fitbit.getStepsFromDate(date);
        talosApi.storeData(u, query);
    }

    public void transferDataFloorFromDate(DemoUser u, Date date) throws TalosModuleException, FitbitAPIException {
        FloorQuery query = fitbit.getFloorsFromDate(date);
        talosApi.storeData(u, query);
    }

    public void transferDataCaloriesFromDate(DemoUser u, Date date) throws TalosModuleException, FitbitAPIException {
        CaloriesQuery query = fitbit.getCaloriesFromDate(date);
        talosApi.storeData(u, query);
    }

    public void transferDataDistanceFromDate(DemoUser u, Date date) throws TalosModuleException, FitbitAPIException {
        DistQuery query = fitbit.getDistanceFromDate(date);
        talosApi.storeData(u, query);
    }

    public void transferDataHeartFromDate(DemoUser u, Date date) throws TalosModuleException, FitbitAPIException {
        HeartQuery query = fitbit.getHearthRateFromDate(date);
        talosApi.storeData(u, query);
    }
}
