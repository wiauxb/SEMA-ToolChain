#!/usr/bin/env python3
import monkeyhex  # this will format numerical results in hexadecimal
import logging
from collections import deque
import sys
from .SemaExplorer import SemaExplorer


class SemaExplorerCDFS(SemaExplorer):
    def __init__(
        self,
        simgr,
        max_length,
        exp_dir,
        nameFileShort,
        worker,
    ):
        super(SemaExplorerCDFS, self).__init__(
            simgr,
            max_length,
            exp_dir,
            nameFileShort,
            worker.scdg,
            worker.call_sim,
            worker.eval_time,
            worker.timeout,
            worker.max_end_state,
            worker.max_step,
            worker.timeout_tab,
            worker.jump_it,
            worker.loop_counter_concrete,
            worker.jump_dict,
            worker.jump_concrete_dict,
            worker.max_simul_state,
            worker.max_in_pause_stach,
            worker.print_on,
            worker.print_sm_step,
            worker.print_syscall,
            worker.debug_error,
        )
        self.pause_stash = deque()
        self.log = logging.getLogger("SemaExplorerCDFS")
        self.log.setLevel("INFO")

    def step(self, simgr, stash="active", **kwargs):
        try:
            simgr = simgr.step(stash=stash, **kwargs)
        except Exception as inst:
            self.log.warning(inst)  # __str__ allows args to be printed directly,
            exc_type, exc_obj, exc_tb = sys.exc_info()
            # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.log.warning(exc_type)
            self.log.warning(exc_obj,exc_type)
            #exit(-1)
            #raise Exception("ERROR IN STEP() - YOU ARE NOT SUPPOSED TO BE THERE !")

        super().build_snapshot(simgr)

        if self.print_sm_step and (
            len(self.fork_stack) > 0 or len(simgr.deadended) > self.deadended
        ):
            self.log.info(
                "A new block of execution have been executed with changes in sim_manager."
            )
            self.log.info("Currently, simulation manager is :\n" + str(simgr))
            self.log.info("pause stash len :" + str(len(self.pause_stash)))

        if self.print_sm_step and len(self.fork_stack) > 0:
            self.log.info("fork_stack : " + str(len(self.fork_stack)) + " " + hex(simgr.active[0].addr) + " || " + hex(simgr.active[1].addr))
            
        # if self.print_sm_step:
        #    self.log.info("len(self.loopBreak_stack) : " + str(len(self.loopBreak_stack)))
        #    self.log.info("state.globals['n_steps'] : " + str(state.globals['n_steps']))

        # We detect fork for a state
        super().manage_fork(simgr)

        simgr.move(
            from_stash="active",
            to_stash="deadend",
            filter_func=lambda s: s.addr == 0xdeadbeef,
        )
        
        # Remove state which performed more jump than the limit allowed
        super().remove_exceeded_jump(simgr)
        
        super().manage_end_thread(simgr)
        
        super().manage_lost(simgr)

        # Manage ended state
        super().manage_deadended(simgr)
        

        for s in simgr.active:
            vis_addr = str(self.check_constraint(s, s.history.jump_target))
            id_to_stash = []
            if vis_addr not in self.dict_addr_vis:
                id_to_stash.append(s.globals["id"])
            simgr.move(
                from_stash="active",
                to_stash="new_addr",
                filter_func=lambda s: s.globals["id"] in id_to_stash,
            )

        super().mv_bad_active(simgr)
        # import pdb; pdb.set_trace()

        if len(simgr.active) > self.max_simul_state:
            excess = len(simgr.active) - self.max_simul_state
            while excess > 0:
                self.pause_stash.append(simgr.active.pop())
                excess = excess - 1
        if len(simgr.stashes["new_addr"]) > 0:
            count = min(len(simgr.active), len(simgr.stashes["new_addr"]))
            while count > 0:
                self.pause_stash.append(simgr.active.pop())
                count = count - 1
        while (
            len(simgr.stashes["new_addr"]) > 0
            and len(simgr.active) < self.max_simul_state
        ):
            simgr.active.append(simgr.stashes["new_addr"].pop())
            self.log.info("Hey new addr !")
        while len(simgr.active) < self.max_simul_state and len(self.pause_stash) > 0:
            simgr.active.append(self.pause_stash.pop())

        # If limit of simultaneous state is not reached and we have some states available in pause stash
        if len(simgr.stashes["pause"]) > 0 and len(simgr.active) < self.max_simul_state:
            moves = min(
                self.max_simul_state - len(simgr.active),
                len(simgr.stashes["pause"]),
            )
            for m in range(moves):
                super().take_longuest(simgr, "pause")

        super().manage_pause(simgr)

        super().drop_excessed_loop(simgr)

        # If states end with errors, it is often worth investigating. Set DEBUG_ERROR to live debug
        # TODO : add a log file if debug error is not activated
        super().manage_error(simgr)

        super().manage_unconstrained(simgr)

        for vis in simgr.active:
            self.dict_addr_vis[
                str(super().check_constraint(vis, vis.history.jump_target))
            ] = 1

        for s in simgr.stashes["new_addr"]:
            vis_addr = str(self.check_constraint(s, s.history.jump_target))
            id_to_stash = []
            if vis_addr in self.dict_addr_vis:
                self.log.info("YOU ARE NOT SUPPOSED TO BE THERE !!!!!!")
                id_to_stash.append(s.globals["id"])
            simgr.move(
                from_stash="new_addr",
                to_stash="temp",
                filter_func=lambda s: s.globals["id"] in id_to_stash,
            )
            moves = len(simgr.stashes["temp"])
            for i in range(moves):
                self.pause_stash.append(simgr.stashes["temp"].pop())

            
        super().excessed_step_to_active(simgr)

        super().excessed_loop_to_active(simgr)

        super().time_evaluation(simgr)

        return simgr
