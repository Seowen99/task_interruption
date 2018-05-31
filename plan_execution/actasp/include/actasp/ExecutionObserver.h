#ifndef actasp_ExecutionObserver_h__guard
#define actasp_ExecutionObserver_h__guard

#include <actasp/AspRule.h>

#include <vector>

namespace actasp {

class AspFluent;
class AnswerSet;
class PartialPolicy;

struct ExecutionObserver {

  virtual void actionStarted(const AspFluent& action) noexcept =0 ;
  virtual void actionTerminated(const AspFluent& action) noexcept =0;
  
  virtual void goalChanged(const std::vector<actasp::AspRule>& newGoalRules) noexcept = 0;
  
  //TODO move this into a separate observer
  virtual void policyChanged(PartialPolicy* policy) noexcept = 0;

  virtual ~ExecutionObserver() {}
};

}


#endif